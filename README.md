# 💸 ExpenseManager

A modern personal finance management system built with Flask. Supports secure user registration and login, transaction tracking, report generation, file uploads, and sharing with others.

![Python](https://img.shields.io/badge/Python-3.8-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-black?logo=flask)
[![License](https://img.shields.io/github/license/Jeffrey86Wan/CITS5505_Group48)](https://github.com/Jeffrey86Wan/CITS5505_Group48/blob/main/LICENSE)
![Issues](https://img.shields.io/github/issues/Jeffrey86Wan/CITS5505_Group48)
![Last Commit](https://img.shields.io/github/last-commit/Jeffrey86Wan/CITS5505_Group48)

---

## ✨ Features

- 🔐 User Authentication (Login/Register)
- 📁 Upload PDF bank statements
- 🤖 GPT-based expense categorization
- 📊 Visual and downloadable reports
- 📤 Share reports with other users

---

## 📁 Project Structure

```
ExpenseManager/
├── app.py                  # Main Flask application entry point
├── db.py                   # Database configuration
├── models/                 # Data models
├── routes/                 # Route modules (user, report, upload, etc.)
│   ├── home.py
│   ├── record.py
│   ├── report.py
│   ├── upload.py
│   ├── api.py
│   └── auth/               # Authentication-related routes
├── templates/              # Frontend templates
│   ├── components/         # Base templates
│   ├── errors/             # Error page templates
│   ├── auth/               # Login and registration templates
│   ├── main/               # Main feature page templates
│   └── partials/           # Partial templates
├── static/                 # Static resources (CSS/JS/images)
├── requirements.txt        # Python dependencies
├── alembic.ini             # Alembic config (DB migration)
├── migrations/             # Database migration scripts
├── seed.py                 # Initialization/test data script
└── README.md
```

---

## ⚙️ Environment Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ExpenseManager.git
cd ExpenseManager
```

### 2. Create Virtual Environment and Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate   # For Windows

pip install -r requirements.txt
```

### 3. Initialize the Database
```bash
# Method 1: Auto-create on first Flask run
python app.py

# Method 2: Use Flask CLI
flask init-db

# Method 3: Alembic migrations
alembic upgrade head
```

### 4. Seed Test Data
```bash
python seed.py
```

---

## ▶️ Run the App
```bash
python app.py
# or
flask run
```

---

## 🌐 Default URL

```
http://127.0.0.1:5000/
```

---

## 📸 Screenshots

> ![alt text](image-3.png)![alt text](image-1.png)![alt text](image-2.png)

---

## 🔁 Reset the Database

To reset:
```bash
flask delete-db
python app.py
```

---

## 📚 References

- [Authentication Design Document (Google Doc)](https://docs.google.com/document/d/your-doc-id/edit)
- Grinberg, M. — [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [W3Schools CSS](https://www.w3schools.com/css/)
- [OpenAI ChatGPT](https://chatgpt.com/)
- [GitHub Docs](https://docs.github.com/)
- Lecture notes and textbook.

---

_Last updated: 2025-05-16_

