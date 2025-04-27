from flask import Blueprint, render_template, request, redirect, jsonify
import os
from werkzeug.utils import secure_filename
from models import db, Expense, Upload
from helpers.parse import parse_amount
from helpers.prompt import build_prompt
from services.chatgpt_service import send_to_chatgpt
from services.pdf_service import extract_text_from_pdf
from dateutil import parser as date_parser
from datetime import datetime
import json

main_bp = Blueprint('main', __name__)

# Home page
@main_bp.route('/')
def index():
    return render_template('index.html')

# Upload page (GET = show form, POST = process file)
@main_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('pdf')
        if not file:
            return 'No file uploaded', 400

        filename = secure_filename(file.filename)
        filepath = os.path.join('uploads', filename)
        file.save(filepath)
        
        # Save filename
        with open('parsed_filename.txt', 'w', encoding='utf-8') as f:
            f.write(filename)

        full_text = extract_text_from_pdf(filepath)
        prompt = build_prompt(full_text)
        expenses_chunk = send_to_chatgpt(prompt)

        # Save temporary result in session or local file (for now, let's use local file)
        with open('parsed_expenses.json', 'w', encoding='utf-8') as f:
            json.dump(expenses_chunk, f, indent=2)

        print(f"✅ Parsed {len(expenses_chunk)} expenses. Redirecting to edit page.")
        return redirect('edit-upload')

    else:
        return render_template('upload.html')

# Edit upload page (before committing to database)
@main_bp.route('/edit-upload', methods=['GET', 'POST'])
def edit_upload():
    if request.method == 'POST':
        try:
            # Load data from the request using get_json() which is a Flask method to parse JSON data
            data = request.get_json()
            
            #read the filename from the temporary file and save it to the database
            if os.path.exists('parsed_filename.txt'):
                with open('parsed_filename.txt', 'r', encoding='utf-8') as f:
                    real_filename = f.read().strip()
            else:
                real_filename = 'manual_upload'  # fallback just in case

            # Gets file name and date from the request
            upload = Upload(filename=real_filename, uploaded_at=datetime.utcnow())
            db.session.add(upload)
            db.session.flush()
            # end of saving filename

            
            new_items = 0
            duplicates = 0
            # Process if data is not emppty and date abides by the format and amount converts to float before saving to db
            for item in data:
                amount = parse_amount(item.get('amount'))
                if amount is None or not item.get('description'):
                    continue
                
                try:
                    parsed_date = date_parser.parse(item['date'], dayfirst=True).date() if item.get('date') else None
                except Exception:
                    parsed_date = None

                # Build the expense object
                expense = Expense(
                    description=item['description'],
                    amount=amount,
                    category=item.get('category', 'Uncategorized'),
                    date=parsed_date,
                    type=item['type'],
                    upload_id=upload.id
                )
                
                # Check server for duplicates before saving
                existing_expense = Expense.query.filter_by(
                date=parsed_date,
                description=item['description'].strip(),
                amount=amount,
                type=item['type']
                ).first()

                if existing_expense:
                    duplicates += 1
                    print(f"⚠️ Duplicate found, skipping: {item}")
                    continue  # Don't save duplicate
                # end of checking for duplicates
                
                db.session.add(expense)
                new_items += 1
            db.session.commit()
            
            # ✅ AFTER success → Clear temporary files
            if os.path.exists('parsed_expenses.json'):
                os.remove('parsed_expenses.json')
                print("✅ Cleared parsed_expenses.json after saving.")
            if os.path.exists('parsed_filename.txt'):
                os.remove('parsed_filename.txt')
                print("✅ Cleared parsed_filename.txt after saving.")
            
            # return a success message by jsonify which is a Flask method to convert Python objects to JSON otherwise it will return a string which causes an error
            return jsonify({
                "status": "success",
                "message": f"Expenses saved successfully! {new_items} new items, {duplicates} duplicates skipped."  
            }), 200


        except Exception as e:
            return jsonify({"error": str(e)}), 500

    else:
        # Load from the temporary file
        if os.path.exists('parsed_expenses.json'):
            with open('parsed_expenses.json', 'r', encoding='utf-8') as f:
                expenses = json.load(f)
        else:
            expenses = []

        return render_template('edit_upload.html', expenses=expenses)
    

