# app.py

from flask import Flask, render_template, request, jsonify # import jsonify for JSON responses and request for handling requests and responses and render_template for rendering HTML templates
from werkzeug.utils import secure_filename # import secure_filename for secure file handling
from dotenv import load_dotenv # import load_dotenv for loading environment variables
import os
import re
import PyPDF2
import openai
import json
import demjson3
from models import db, Expense, Upload # import db, Expense, and Upload from models.py
from datetime import datetime
from dateutil import parser as date_parser

def parse_amount(value):
    try:
        return float(str(value).replace('$', '').replace(',', ''))
    except ValueError:
        return None

# create a Flask application instance
app = Flask(__name__) 
# the key tells Flask where to store uploaded files
app.config['UPLOAD_FOLDER'] = 'uploads' 
# key: tells SQLAlchemy to use SQLite as db and the value is the path to the db file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
# key: tells SQLAlchemy to track modifications of objects & emit signals
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# key: tells Flask to use the secret key for session management and CSRF protection
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

load_dotenv()
# Set OpenAI client
client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

db.init_app(app) # initialize the database with the Flask app
with app.app_context():
    db.create_all()

#@app.before_first_request  # this function is called before the first request to the application
#def create_tables():
#    db.create_all()

@app.route('/') # when get request is made to the root URL do the following
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST']) #when post request is made to /upload do the following
def upload():
    file = request.files.get('pdf')
    if not file:
        return 'No file uploaded', 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Extract text from PDF
    reader = PyPDF2.PdfReader(filepath)
    full_text = "\n".join([page.extract_text() or '' for page in reader.pages])
    
    with open("extracted_pdf_text_after.txt", "w", encoding="utf-8") as f:
        f.write(full_text)
        
    print(f"🧹 Extracted {len(reader.pages)} pages from PDF")


    # Prepare the entire text as one chunk
    chunk_text = full_text

    # send big prompt to ChatGPT
            
    prompt = f"""
    Extract each expense line item from the following bank statement text. Return a **valid JSON array only** — no explanations, headings, markdown, or extra text — just the JSON array.

    Each item must include the following fields:
    - "date": The transaction date in ISO format (YYYY-MM-DD), or null if not found.
    - "description": A concise human-readable description of the transaction.
    - "amount": A float with no currency symbols or commas (e.g., 256.00).
    - "type": Use "debit" for expenses or payments made, and "credit" for incoming funds or refunds.
    Some bank statements use two separate columns (Debit and Credit). Use the description name or sign of the amount values to decide the type.
    - "category": Choose the most appropriate category based on your knowldege. If you do not recognize the merchant, do your best to infer the most likely category from the name/description. ou must guess categories even if you're unsure. Use general knowledge

    Bank statement text may come from various formats: table rows, CSV, natural sentences, etc. Detect and normalize them.

    Bank statement text:
    {chunk_text}
    """

   
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
        
    raw_chunk = response.choices[0].message.content.strip()

    # Save raw GPT output
    with open("raw_chatgpt_response.txt", "w", encoding="utf-8") as f:
        f.write(raw_chunk)
        
    try:
        # 🧹 Clean top and bottom junk if any
        first_bracket = raw_chunk.find('[')
        last_bracket = raw_chunk.rfind(']')
        if first_bracket != -1 and last_bracket != -1:
            raw_chunk = raw_chunk[first_bracket:last_bracket+1]

        # 🧹 Normalize quotation marks and commas inside numbers
        raw_chunk = raw_chunk.replace("“", '"').replace("”", '"')
        raw_chunk = raw_chunk.replace("‘", "'").replace("’", "'").replace("`", "'")
        raw_chunk = re.sub(
            r'("amount"\s*:\s*")(\d{1,3}(,\d{3})+(\.\d+)?)(")',
            lambda m: f'{m.group(1)}{m.group(2).replace(",", "")}{m.group(5)}',
            raw_chunk
        )

        expenses_chunk = demjson3.decode(raw_chunk)

        # ✅ Fix type for direct debits or negative values
        for item in expenses_chunk:
            if 'direct debit' in item['description'].lower() or (item.get('amount') and float(item['amount']) < 0):
                item['type'] = 'credit'
            else:
                item['type'] = 'debit'

        print(f"✅ GPT returned {len(expenses_chunk)} items")

    except demjson3.JSONDecodeError as e:
        return f"❌ demjson3 JSON Error: {e}<br><br><pre>{raw_chunk}</pre>", 500


        
    upload = Upload(filename=file.filename, uploaded_at=datetime.utcnow())
    db.session.add(upload)
    db.session.flush()

    skipped_items = []  # ✅ Store skipped items for later logging
    print(f"📊 Total categorized items from ChatGPT: {len(expenses_chunk)}")

    for item in expenses_chunk:
        
        #  Skip balance line
        if item['description'].strip().lower() == "opening balance":
            print(f"⚠️ Skipping opening balance: {item}")
            skipped_items.append(item)
            continue
        

        # Then sanitize and validate amount + description
        amount = parse_amount(item.get('amount'))
        if amount is None or not item.get('description'):
            print(f"⚠️ Skipping item with issues: {item}")
            skipped_items.append(item)
            continue

        item['category'] = item.get('category') or 'Uncategorized'
        
        # Handle date parsing
        try:
            parsed_date = date_parser.parse(item['date'], dayfirst=True).date() if item.get('date') else None
        except Exception:
            parsed_date = None

        expense = Expense(
            description=item['description'],
            amount=amount,
            category=item['category'],
            date=parsed_date,
            type=item['type'],
            upload_id=upload.id
        )
        db.session.add(expense)
                
    if skipped_items:
        with open("skipped_items.json", "w") as f:
            json.dump(skipped_items, f, indent=2)
                
    db.session.commit()
    return jsonify(expenses_chunk)
                    
if __name__ == '__main__':
    print("✅ App started, initializing DB...")
    with app.app_context():
        db.create_all()
    print("✅ DB initialized, starting Flask...")
    app.run(debug=True, port=5000)