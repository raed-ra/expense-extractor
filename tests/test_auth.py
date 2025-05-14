"""
测试登录功能
"""
import unittest
from models import User
from flask_login import current_user
from tests.test_config import TestConfig
from app import create_app
from db import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash

class TestAuth(unittest.TestCase):
    """test login function"""
    
    @classmethod
    def setUpClass(cls):
        """setup before test class"""
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
        
    @classmethod
    def tearDownClass(cls):
        """tear down after test class"""
        # restore original get_db function
        if hasattr(cls, 'original_get_db'):
            cls.app.view_functions['get_db'] = cls.original_get_db
            
        # clean up database
        Base.metadata.drop_all(cls.engine)
        
        # clean up app context
        cls.app_context.pop()
        
    def setUp(self):
        """setup before test method"""
        # create test client
        self.client = self.app.test_client()
        
        # create new test database session
        self.db = self.session_factory()
        
        # override get_db function to use test database
        def _get_test_db():
            return self.db
        
        self.app.view_functions['get_db'] = _get_test_db
        
    def tearDown(self):
        """tear down after test method"""
        # rollback all changes during test
        self.db.rollback()
        self.db.close()
        
    def test_login_page(self):
        """test login page"""
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'login', response.data.lower())

    def test_register_and_login(self):
        """test register and login process"""
        # test user data
        test_username = 'testuser'
        test_email = 'test@example.com'
        test_password = 'password123'
        
        # create user and save to database (not through route)
        hashed_password = generate_password_hash(test_password)
        user = User(username=test_username, email=test_email, password=hashed_password)
        self.db.add(user)
        self.db.commit()
        
        # verify user added to database
        user_check = self.db.query(User).filter_by(email=test_email).first()
        self.assertIsNotNone(user_check)
        self.assertEqual(user_check.username, test_username)
        
        # test login with wrong password
        response = self.client.post('/auth/login', data={
            'email': test_email,
            'password': 'wrong_password'
        }, follow_redirects=True)
        
        # should fail
        self.assertTrue(b'invalid' in response.data.lower() or b'incorrect' in response.data.lower())
        
        # test login with correct credentials
        response = self.client.post('/auth/login', data={
            'email': test_email,
            'password': test_password
        }, follow_redirects=True)
        
        # login should succeed and redirect to dashboard
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'dashboard' in response.data.lower() or b'welcome' in response.data.lower())
        
        # check if user is logged in
        with self.client.session_transaction() as session:
            self.assertIn('_user_id', session)  # Flask-Login session key for user ID
            self.assertIn('user_id', session)   # custom session key for user ID
            
if __name__ == '__main__':
    unittest.main()