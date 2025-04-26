# CITS5505_Group48
UWA Agile Web Development Project


# 📄 Expense Extractor App (Sample Project)

This small Flask web app lets you upload a **PDF bank statement**, send it to **ChatGPT** for categorization, and review the transactions on a webpage.  
(Everything runs locally on your machine. Your data and OpenAI key stay private.)

---

## 🚀 Setup Guide

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### 2. Create and Activate a Virtual Environment (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

Install all required Python packages in one command:

```bash
pip install -r requirements.txt
```

(This installs Flask, OpenAI, SQLAlchemy, PyPDF2, demjson3, and others.)

---

## 🔑 Set Up Your OpenAI API Key

1. Create a `.env` file in the project root directory.
2. Add this line inside `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

You can get your API key from https://platform.openai.com/account/api-keys.

⚠️ **Important:**  
Each person must use **their own API key**.  
The key is private and not shared with anyone else.

---

## 🖥️ How to Run the App

Once setup is done:

```bash
flask run
```

or

```bash
python app.py
```

Then open your browser and go to:

```
http://127.0.0.1:5000/
```

✅ Now you can upload a bank statement and try it!

---

## 📚 Current Features

- Upload a PDF bank statement.
- Extract raw text from PDF.
- Send extracted text to OpenAI's GPT model.
- Parse and clean ChatGPT's response into JSON.
- Display transactions in a basic table.

---

## 🔥 What’s Coming Next?

I'm currently working on:
- A new page where **you can edit** the transactions before saving.
- Adding a **"New Entry"** button to manually add transactions.
- **Delete** individual transaction rows easily.

Once the basic edit/save features are done,  
we will move to the **frontend polishing** and **reports/graphs dashboard**.

---



