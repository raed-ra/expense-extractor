"""
test record function
"""
import unittest
from flask import url_for
from app import create_app
from tests.test_config import TestConfig
from db import Base, get_db
from models.user import User
from models.transaction import Transaction
from flask_login import login_user
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug.security import generate_password_hash

class TestRecord(unittest.TestCase):
    """test record function"""

    @classmethod
    def setUpClass(cls):
        """test class setup before"""
        # create test app
        cls.app = create_app()
        cls.app.config.from_object(TestConfig)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        # create in-memory database engine
        cls.engine = create_engine(TestConfig.SQLALCHEMY_DATABASE_URI)
        Base.metadata.create_all(cls.engine)

        # create database session
        cls.session_factory = scoped_session(sessionmaker(bind=cls.engine))

        # store original get_db function
        cls.original_get_db = cls.app.view_functions.get('get_db', get_db)

        # ensure Flask-Login is loaded correctly
        with cls.app.test_request_context():
            pass

        print("test class initialization completed")

    @classmethod
    def tearDownClass(cls):
        """test class cleanup after"""
        # restore original get_db function
        if hasattr(cls, 'original_get_db'):
            cls.app.view_functions['get_db'] = cls.original_get_db

        # clean up database
        print("cleaning up database...")
        try:
            cls.engine.dispose()
            Base.metadata.drop_all(cls.engine)
            print("database cleanup completed")
        except Exception as e:
            print(f"database cleanup failed: {e}")

        # clean up app context
        cls.app_context.pop()
        print("app context cleaned up")

    def setUp(self):
        """test method setup before"""
        # create test client
        self.client = self.app.test_client()

        # create new test database session
        self.db = self.session_factory()

        # override get_db function to use test database
        def _get_test_db():
            return self.db

        self.app.view_functions['get_db'] = _get_test_db

        # check and delete possible existing test user
        try:
            existing_user = self.db.query(User).filter_by(email='test@example.com').first()
            if existing_user:
                self.db.delete(existing_user)
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(f"Error clearing existing user: {e}")

        # create test user
        try:
            hashed_password = generate_password_hash('password')
            user = User(username='testuser', email='test@example.com', password=hashed_password)
            self.db.add(user)
            self.db.commit()

            # get the newly created user
            self.test_user = self.db.query(User).filter_by(email='test@example.com').first()
            print(f"Test user created successfully: ID={self.test_user.id}, username={self.test_user.username}")

            # login test user
            with self.client as c:
                with c.session_transaction() as session:
                    session['user_id'] = self.test_user.id
                    session['_user_id'] = str(self.test_user.id)  # Flask-Login needs string

                # login user in test request context
                with self.app.test_request_context():
                    login_user(self.test_user)

                # ensure session is saved
                c.preserve_context_on_exception = False

            print(f"User {self.test_user.username} logged in successfully")

        except Exception as e:
            self.db.rollback()
            print(f"Error creating test user: {e}")

    def tearDown(self):
        """test method cleanup after"""
        try:
            # delete all test created transaction records
            if hasattr(self, 'test_user'):
                transactions = self.db.query(Transaction).filter_by(user_id=self.test_user.id).all()
                for transaction in transactions:
                    self.db.delete(transaction)

            # delete test user
            user = self.db.query(User).filter_by(email='test@example.com').first()
            if user:
                self.db.delete(user)

            # commit changes
            self.db.commit()
        except Exception as e:
            print(f"Error cleaning up data: {e}")
            self.db.rollback()
        finally:
            # close session
            self.db.close()

    def test_record_creation_success(self):
        """test successful record creation"""
        print("\nStarting test for successful record creation...")

        response = self.client.get('/record/')
        self.assertEqual(response.status_code, 200, "Should access the record page")
        print("Verified record page access successfully")

        # Clear previous possible records
        try:
            existing_records = self.db.query(Transaction).filter_by(description='Grocery shopping').all()
            for record in existing_records:
                self.db.delete(record)
            self.db.commit()
            print(f"Cleared {len(existing_records)} old records")
        except Exception as e:
            self.db.rollback()
            print(f"Failed to clear old records: {e}")

        # Submit create record request
        form_data = {
            'amount': '100.00',
            'category': 'Food',
            'date': '2023-01-01',
            'description': 'Grocery shopping',
            'record_type': 'expense'
        }

        response = self.client.post('/record/', data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        error_messages = ['Amount cannot be empty', 'Category cannot be empty', 'Date cannot be empty']
        for error in error_messages:
            self.assertNotIn(error, response_text, f"Response should not contain error message: {error}")

        print("Test success: No error messages in response")

if __name__ == '__main__':
    unittest.main()
