# ExpenseManager

ExpenseManager is a modern personal finance management system that supports user registration, login, transaction recording, report analysis, data upload, and sharing.

## Project Structure

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

## Environment Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ExpenseManager
   ```

2. **Create a virtual environment and install dependencies**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate

   pip install -r requirements.txt
   ```

3. **Initialize the database**
   - **Method 1: Auto-initialize**  
     The database and tables will be created automatically when you start Flask for the first time.
   - **Method 2: Using Flask CLI command (if registered)**  
     ```bash
     flask init-db
     ```
   - **Method 3: Using Alembic migration (if migration scripts exist)**  
     ```bash
     alembic upgrade head
     ```

4. **Seed real database with test data script**
    ```bash
     python3 seed.py
     ```

## Run the Project

```bash
python app.py
```
or
```bash
flask run
```

Default access: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Additional Notes

- To reset the database, simply delete the `expensemanager.db` file and restart the project to auto-recreate it.
- For more features and usage, please refer to the source code of each module. 
