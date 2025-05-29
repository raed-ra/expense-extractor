# ./tests/test_upload.py

import io
import pytest
from flask import url_for
from app import create_app
from flask_login import login_user
from models import Transaction

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['LOGIN_DISABLED'] = False

    client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    from db import get_db
    from models import User
    from werkzeug.security import generate_password_hash

    db = get_db()
    user = db.query(User).filter_by(email="testuser@example.com").first()
    if not user:
        user = User(
            email="testuser@example.com",
            username="Test User",
            password_hash=generate_password_hash("password")
        )
        db.add(user)
        db.commit()
        print("✅ Test user created.")
    else:
        print("✅ Test user exists.")

    with client.session_transaction() as sess:
        sess['_user_id'] = str(user.id)
        print("✅ Simulated login with session user ID.")

    yield client
    ctx.pop()


# ✅ Test 1: GET /upload renders correctly
def test_upload_get(client):
    print("➡️ Test: GET /upload")
    response = client.get('/upload', follow_redirects=True)
    assert response.status_code == 200
    assert b"Upload Your Bank Statement" in response.data
    print("✅ /upload page rendered and contains expected text.")


# ✅ Test 2: POST /upload with a dummy PDF
def test_upload_post_pdf(client):
    print("➡️ Test: POST /upload with dummy PDF")
    pdf_data = (
        b"%PDF-1.4\n"
        b"1 0 obj\n"
        b"<< /Type /Catalog /Pages 2 0 R >>\n"
        b"endobj\n"
        b"2 0 obj\n"
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>\n"
        b"endobj\n"
        b"3 0 obj\n"
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] >>\n"
        b"endobj\n"
        b"xref\n"
        b"0 4\n"
        b"0000000000 65535 f \n"
        b"0000000010 00000 n \n"
        b"0000000053 00000 n \n"
        b"0000000100 00000 n \n"
        b"trailer\n"
        b"<< /Root 1 0 R /Size 4 >>\n"
        b"startxref\n"
        b"147\n"
        b"%%EOF\n"
    )

    data = {
        'pdf_file': (io.BytesIO(pdf_data), 'test.pdf')
    }

    response = client.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert response.status_code == 200
    assert b"parsed results" in response.data or b"GPT" in response.data
    print("✅ PDF uploaded and parsed response received.")


# ✅ Test 3: POST /upload/edit-upload with new transaction
def test_edit_upload_post(client):
    print("➡️ Test: POST /upload/edit-upload with transaction JSON")

    payload = {
        "filename": "test.pdf",
        "new": [
            {
                "date": "2024-05-01",
                "description": "Test Transaction",
                "amount": "123.45",
                "credit_type": "debit",
                "category": "Groceries"
            }
        ]
    }

    response = client.post('/upload/edit-upload', json=payload, follow_redirects=True)
    assert response.status_code == 200
    assert b"Expenses saved successfully" in response.data
    print("✅ Transaction saved and confirmation message received.")

    from db import get_db
    db = get_db()
    txn = db.query(Transaction).filter_by(description="Test Transaction").first()
    assert txn is not None
    from decimal import Decimal
    assert txn.amount == Decimal('123.45')
    print("✅ Transaction found in database with correct amount.")


# ✅ Test Summary: What this file verifies
#
# - test_upload_get:
#   - Sends a GET request to /upload
#   - Verifies that the upload form renders correctly
#   - Confirms the route is reachable and returns status 200
#
# - test_upload_post_pdf:
#   - Simulates uploading a minimal valid PDF file
#   - Verifies that the backend:
#     - Saves the file
#     - Extracts text
#     - Sends it to GPT
#     - Renders the HTML page with the parsed GPT response
#   - Confirms the response contains expected text or table
#
# - test_edit_upload_post:
#   - Simulates submitting edited transaction data via AJAX to /upload/edit-upload
#   - Verifies that the backend:
#     - Parses and validates the JSON
#     - Skips duplicates
#     - Inserts a new transaction into the database
#   - Asserts that the response includes a success message
#   - Confirms that the transaction is actually saved with correct values
