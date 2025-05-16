import pytest
from app import create_app
from db import get_db, Base, engine
from models import User
from werkzeug.security import generate_password_hash

# ✅ Import the blueprint
from routes.report import report_bp

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "LOGIN_DISABLED": False
    })

    # DO NOT register blueprints if they are already registered in create_app()

    with app.app_context():
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        db = get_db()

        # Add both test users
        db.add_all([
            User(
                email="test@example.com",
                password=generate_password_hash("test123"),
                username="TestUser"
            ),
            User(
                email="testuser2@example.com",
                password=generate_password_hash("test456"),
                username="Recipient"
            )
        ])
        db.commit()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth(client):
    def login():
        return client.post("/auth/login", data={
            "email": "test@example.com",
            "password": "test123"
        }, follow_redirects=True)
    return login

