# 📄 Expense Extractor App (Sample Project)

This small Flask web app lets you upload a **PDF bank statement**, send it to **ChatGPT** for categorization, and review and edit the transactions before saving them to a local database.  
(Everything runs **locally**. Your **bank data** and **OpenAI key** stay **private**.)

---

## 🚀 Setup Guide

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

(If you're on a different branch, don't forget to check it out:  
`git checkout your-branch-name`)

### 2. Create and Activate a Virtual Environment (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

(This installs Flask, SQLAlchemy, OpenAI, PyPDF2, demjson3, python-dotenv, etc.)

---

## 🔑 Set Up Your OpenAI API Key

1. Create a `.env` file in the project root.
2. Inside `.env`, add:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

You can create an API key at: [OpenAI Platform](https://platform.openai.com/account/api-keys)

⚠️ **Important:**  
Everyone uses their own API key!  
The key remains private and is never stored on the server.

---

## 🖥️ How to Run the App

```bash
flask run
```
or

```bash
python app.py
```

Then open your browser:

```
http://127.0.0.1:5000/
```

✅ You should see the homepage where you can **choose to upload** a bank statement.

---

## 📚 Current Features

- Upload a PDF bank statement.
- Extract raw text using **PyPDF2**.
- Send extracted text to **OpenAI GPT model**.
- Categorize transactions using ChatGPT.
- Edit transactions manually before saving (Add ➕, Delete 🗑️, Update ✏️).
- Save edited transactions into an **SQLite database** (via SQLAlchemy).
- Temporary files like parsed data are **cleared automatically** after saving.

---

## 🛤️ App Flow Overview

| Step | What Happens | Frontend Page | Backend Action |
|:----:|:-------------|:-------------:|:--------------:|
| 1 | Visit homepage | `/` | Choose to upload |
| 2 | Upload PDF | `/upload` | Extract + Send to GPT |
| 3 | Review & Edit | `/edit-upload` | Modify/Add/Delete transactions |
| 4 | Submit | (AJAX POST) | Save to database |

---

## 🔥 What's Coming Next?

- **Manage Transactions** page:  
  View, edit, delete existing saved transactions.
- **Reports / Analytics** dashboard:  
  Monthly summaries, category spendings.
- **Better Mobile View** with responsive Bootstrap.
- **Authentication (optional phase):**  
  Login system for users (optional bonus later).

---

## 📂 Folder Structure (Important)

```bash
app.py
models.py
/helpers
    parse.py
    prompt.py
/services
    chatgpt_service.py
    pdf_service.py
/routes
    main.py
/templates
    index.html
    upload.html
    edit_upload.html
/static/js
    index.js
    edit.js
uploads/  (uploaded PDFs stored temporarily)
database.db (SQLite)
parsed_expenses.json (temporary parsed data)
parsed_filename.txt (temporary uploaded filename)
```

---

## ⚙️ Development Branch

This project has multiple branches:

- `main`: Stable version
- `suggestion-project-rr` (example): Experimental / upgraded version (use for testing!)

✅ Always pull or push to the correct branch!

---

# ✨ Enjoy!  
If you have questions, open an issue or contact the repo maintainer 🚀

