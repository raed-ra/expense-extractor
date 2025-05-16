# ./tests/test_upload.py

import io
from flask import url_for
from app import create_app  # or your app factory
from models import User
import pytest

@pytest.fixture
def client():
    app = create_app()  # or however you configure test mode
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['LOGIN_DISABLED'] = True  # if using flask-login
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield client
    ctx.pop()

def test_upload_get(client):
    response = client.get('/upload', follow_redirects=True)
    assert response.status_code == 200
    assert b"Upload Your Bank Statement" in response.data

def test_upload_post_pdf(client):
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
