# CITS5505_Group48
UWA Agile Web Development Project


# 📚 Project Setup Guide

Welcome! 👋\
Follow these simple steps to set up and run the **PDF Bank Statement Parser** locally.

---

## 🚀 Prerequisites

1. **Python 3.8+** installed on your machine.
2. **OpenAI account** with an **API key**.
3. **Basic command-line skills** (terminal).

---

## 📂 Project Folder Structure

```bash
/your-project-folder/
│
├── app.py
├── models.py
├── /templates/
│    └── index.html
├── /static/
│    ├── upload.js
│    ├── edit.js
│    └── (optional) styles.css
├── extracted_pdf_text_after.txt  # (auto-created)
├── raw_chatgpt_response.txt      # (auto-created)
├── saved_chatgpt_response.json   # (auto-created)
├── skipped_items.json            # (auto-created)
├── database.db                   # (auto-created SQLite DB)
└── .env
```

---

## 🛆 Step 1: Install Dependencies

Open terminal in your project folder and run:

```bash
pip install flask python-dotenv openai pypdf2 sqlalchemy demjson3 python-dateutil
```

---

## 🔑 Step 2: Setup your OpenAI API Key

1. Go to [platform.openai.com](https://platform.openai.com/account/api-keys)
2. Create a new API key if you don't have one.
3. In your project folder, create a `.env` file:

```bash
touch .env
```

4. Inside `.env`, paste this line (replace YOUR\_API\_KEY):

```dotenv
OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXX
```

✅ Save and close.

---

## 🛠️ Step 3: Run the App

In terminal, still inside the project folder, run:

```bash
python app.py
```

You should see:

```bash
✅ App started, initializing DB...
✅ DB initialized, starting Flask...
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Then open your browser and visit:

```
http://localhost:5000
```

---

## 🧐 How it Works

- Upload your bank statement PDF.
- App extracts the raw text.
- App sends the text to **ChatGPT** for **smart JSON extraction**.
- A table appears where you can **edit, delete, add** entries.
- When ready, click **Submit** to save all transactions into your **local SQLite database** (`database.db`).

---

## 💡 Notes

- All extracted text and ChatGPT responses are saved locally (`.txt` and `.json` files) for inspection.
- Negative amounts (`-`) or "Direct Debit" descriptions are automatically set to **Credit** type.
- If the JSON from ChatGPT has minor errors, the app tries to **auto-clean** them.
- You **must** have internet access while running (because it uses the ChatGPT API).

---

## 🔥 Coming Features (optional ideas)

- Search transactions by date.
- Download/export transactions to CSV.
- Visual dashboard (total spent, pie charts by category).
- Authentication (login/logout).

---

# ✅ You're ready to go!

