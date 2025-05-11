#service/chatgpt_service.py
import openai
import os
import re
import demjson3
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def send_to_chatgpt(prompt, user_id):
    # Error handling
    try:
        client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        raw_chunk = response.choices[0].message.content.strip()

    except openai.OpenAIError as e:
        # ✅ Optional fallback in development mode
        if os.getenv("FLASK_ENV") == "development":
            print(f"[WARNING] GPT fallback due to error: {e}")
            return [{
                "date": str(datetime.now().date()),
                "description": "Test fallback item",
                "amount": "123.45",
                "type": "debit"
            }]
        else:
            raise RuntimeError(f"GPT call failed: {e}")

    

    # 📂 Create user-specific folder if needed
    output_folder = os.path.join("user_data", f"user_{user_id}")
    os.makedirs(output_folder, exist_ok=True)

    # 💾 Save raw GPT output
    raw_path = os.path.join(output_folder, "raw_chatgpt_response.txt")
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(raw_chunk)

    # 🧹 Clean up response
    first_bracket = raw_chunk.find('[')
    last_bracket = raw_chunk.rfind(']')
    if first_bracket != -1 and last_bracket != -1:
        raw_chunk = raw_chunk[first_bracket:last_bracket+1]

    raw_chunk = raw_chunk.replace("“", '"').replace("”", '"')
    raw_chunk = raw_chunk.replace("‘", "'").replace("’", "'").replace("`", "'")
    raw_chunk = re.sub(
        r'("amount"\s*:\s*")(\d{1,3}(,\d{3})+(\.\d+)?)(")',
        lambda m: f'{m.group(1)}{m.group(2).replace(",", "")}{m.group(5)}',
        raw_chunk
    )

    # 🔁 Decode and enrich
    expenses_chunk = demjson3.decode(raw_chunk)
    for item in expenses_chunk:
        if 'direct debit' in item['description'].lower() or (item.get('amount') and float(item['amount']) < 0):
            item['type'] = 'credit'
        else:
            item['type'] = 'debit'

    return expenses_chunk
