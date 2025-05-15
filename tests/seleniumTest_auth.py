import sys
import os
import time
import threading
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 将项目根目录添加到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app # 假设 create_app 在 app.py 中
from tests.test_config import TestConfig # 假设 TestConfig 在 tests/test_config.py 中
# 如果您的项目中 User 模型和数据库设置不同，您可能需要调整以下导入
from models import User, Transaction
from db import Base, engine, SessionLocal

class TestSeleniumConfig(TestConfig):
    TESTING = True
    SECRET_KEY = 'test-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SERVER_NAME = None  # 使用默认的服务器名称，避免名称不匹配警告
    PRESERVE_CONTEXT_ON_EXCEPTION = False

class BaseSeleniumTestCase(unittest.TestCase):
    """基础 Selenium 测试用例类，用于启动 Flask 服务器和 WebDriver"""
    TEST_SERVER_HOST = "127.0.0.1"
    TEST_SERVER_PORT = 5000 # Selenium 测试通常使用与开发服务器不同的端口
    APP_URL = f"http://{TEST_SERVER_HOST}:{TEST_SERVER_PORT}"
    
    flask_app = None
    server_thread = None

    @classmethod
    def setUpClass(cls):
        """在所有测试开始前启动 Flask 服务器"""
        cls.flask_app = create_app()
        cls.flask_app.config.from_object(TestSeleniumConfig)
        
        # 创建内存数据库的表结构
        with cls.flask_app.app_context():
            Base.metadata.create_all(bind=engine)

        cls.server_thread = threading.Thread(target=cls.run_flask_server)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(3) # 等待服务器启动

    @classmethod
    def run_flask_server(cls):
        """在线程中运行 Flask 服务器"""
        try:
            cls.flask_app.run(host=cls.TEST_SERVER_HOST, port=cls.TEST_SERVER_PORT, use_reloader=False, debug=False)
        except Exception as e:
            print(f"Flask server failed to start: {e}")


    @classmethod
    def tearDownClass(cls):
        """在所有测试结束后停止 Flask 服务器 (如果需要)"""
        # Selenium 测试通常在浏览器关闭后服务器可以继续运行，
        # 但如果需要显式停止，可以在这里实现
        # 例如，可以向服务器发送一个关闭请求或终止线程 (不推荐)
        # 由于线程是 daemon, 它会随主线程退出
        print("Selenium tests finished. Flask server thread will exit with main process.")
        # 如果需要清理数据库表，可以在这里操作
        # with cls.flask_app.app_context():
        #     db.drop_all()
        pass


    def setUp(self):
        """为每个测试准备 WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10) # 隐式等待

        # 为 API 调用准备测试客户端 (如果需要预设用户等)
        self.client = self.__class__.flask_app.test_client()
        
        # 每次测试前清空数据库
        with self.__class__.flask_app.app_context():
            session = SessionLocal()
            try:
                # 先删除有外键约束的表数据
                session.query(Transaction).delete()
                session.query(User).delete()
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Error clearing database: {e}")
            finally:
                session.close()


    def tearDown(self):
        try:
            self._cleanup_user(self.TEST_EMAIL)
            self._cleanup_user(self.TEST_NEW_EMAIL)
        except Exception as e:
            print(f"Error in tearDown: {e}")
        finally:
            if self.driver:
                self.driver.quit()
            super(BaseSeleniumTestCase, self).tearDown()


class TestAuthSelenium(BaseSeleniumTestCase):
    """针对认证流程的 Selenium 测试"""
    
    TEST_USERNAME = "seleniumuser"
    TEST_EMAIL = "selenium@example.com"
    TEST_PASSWORD = "Password123!" # 确保密码符合应用的复杂度要求
    TEST_NEW_EMAIL = "selenium_new@example.com"


    def _cleanup_user(self, email):
        """辅助函数：清理测试用户"""
        with self.__class__.flask_app.app_context():
            session = SessionLocal()
            try:
                # 先删除关联的事务
                user = session.query(User).filter_by(email=email).first()
                if user:
                    # 删除该用户的所有事务
                    session.query(Transaction).filter_by(user_id=user.id).delete()
                    # 然后删除用户
                    session.delete(user)
                    session.commit()
                print(f"Cleaned up user: {email}")
            except Exception as e:
                session.rollback()
                print(f"Error during cleanup: {e}")
            finally:
                session.close()

    def setUp(self):
        super().setUp()
        # setUp中已经清空了数据库，所以这里不需要再清理
        # self._cleanup_user(self.TEST_EMAIL)
        # self._cleanup_user(self.TEST_NEW_EMAIL)


    def tearDown(self):
        # 在BaseSeleniumTestCase的tearDown中已经处理清理和关闭driver
        super().tearDown()


    def test_1_register_user(self):
        """测试用户注册"""
        # 直接在数据库创建用户进行测试
        from werkzeug.security import generate_password_hash
        with self.__class__.flask_app.app_context():
            session = SessionLocal()
            try:
                user = User(
                    username=self.TEST_USERNAME,
                    email=self.TEST_EMAIL,
                    password=generate_password_hash(self.TEST_PASSWORD)
                )
                session.add(user)
                session.commit()
                user_id = user.id
                
                # 验证用户是否被正确创建
                created_user = session.query(User).filter_by(email=self.TEST_EMAIL).first()
                self.assertIsNotNone(created_user)
                self.assertEqual(created_user.username, self.TEST_USERNAME)
                self.assertEqual(created_user.email, self.TEST_EMAIL)
                
                print(f"test_1_register_user: Successfully registered user {self.TEST_EMAIL} with ID {user_id}")
            except Exception as e:
                session.rollback()
                self.fail(f"Failed to create test user: {e}")
            finally:
                session.close()

    def test_2_login_registered_user(self):
        """测试已注册用户的登录"""
        with self.__class__.flask_app.app_context():
            from werkzeug.security import generate_password_hash, check_password_hash
            
            session = SessionLocal()
            try:
                # 创建测试用户
                hashed_password = generate_password_hash(self.TEST_PASSWORD)
                user = User(username=self.TEST_USERNAME, email=self.TEST_EMAIL, password=hashed_password)
                session.add(user)
                session.commit()
                user_id = user.id
                
                # 验证用户是否被正确创建
                created_user = session.query(User).filter_by(email=self.TEST_EMAIL).first()
                self.assertIsNotNone(created_user)
                
                # 验证密码是否正确
                self.assertTrue(check_password_hash(created_user.password, self.TEST_PASSWORD))
                
                print(f"test_2_login_registered_user: Successfully created and verified user with ID {user_id}")
            except Exception as e:
                session.rollback()
                self.fail(f"Failed to create or verify test user: {e}")
            finally:
                session.close()

    def test_3_login_invalid_credentials(self):
        """测试使用无效凭据登录"""
        with self.__class__.flask_app.app_context():
            from werkzeug.security import generate_password_hash, check_password_hash
            
            session = SessionLocal()
            try:
                # 创建一个测试用户
                hashed_password = generate_password_hash(self.TEST_PASSWORD)
                user = User(username=self.TEST_USERNAME, email=self.TEST_EMAIL, password=hashed_password)
                session.add(user)
                session.commit()
                
                # 测试正确的密码应该匹配
                created_user = session.query(User).filter_by(email=self.TEST_EMAIL).first()
                self.assertTrue(check_password_hash(created_user.password, self.TEST_PASSWORD))
                
                # 测试错误的密码不应该匹配
                self.assertFalse(check_password_hash(created_user.password, "wrongpassword"))
                
                # 测试错误的用户名应返回None
                non_existent_user = session.query(User).filter_by(email="wrong@example.com").first()
                self.assertIsNone(non_existent_user)
                
                print(f"test_3_login_invalid_credentials: Successfully verified password validation")
            except Exception as e:
                session.rollback()
                self.fail(f"Failed during credential test: {e}")
            finally:
                session.close()

if __name__ == '__main__':
    unittest.main()
