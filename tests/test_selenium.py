import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import threading
import subprocess
import os
import signal
import sys
import atexit
import requests
from urllib.parse import urljoin

class TestExpenseManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Start the Flask server before all tests."""
        cls.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.base_url = "http://localhost:5000"
        print("Starting Flask server...")
        cls.server_process = subprocess.Popen(
            [sys.executable, '-m', 'flask', 'run'],
            cwd=cls.root_dir,
            env=dict(os.environ, FLASK_APP='app.py', FLASK_ENV='testing'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        max_retries = 10
        retry_count = 0
        while retry_count < max_retries:
            try:
                response = requests.get(urljoin(cls.base_url, '/login'))
                if response.status_code == 200:
                    print("Flask server started successfully!")
                    break
            except requests.exceptions.ConnectionError:
                print(f"Waiting for server to start... ({retry_count + 1}/{max_retries})")
                time.sleep(1)
                retry_count += 1
        else:
            print("Server failed to start!")
            print("Server stdout:")
            print(cls.server_process.stdout.read())
            print("Server stderr:")
            print(cls.server_process.stderr.read())
            cls.tearDownClass()
            raise Exception("Failed to start Flask server")
        atexit.register(cls.tearDownClass)

    @classmethod
    def tearDownClass(cls):
        """Shut down the Flask server after all tests."""
        if hasattr(cls, 'server_process') and cls.server_process:
            try:
                subprocess.run(['taskkill', '/F', '/T', '/PID', str(cls.server_process.pid)])
            except Exception as e:
                print(f"Error shutting down server: {e}")
            finally:
                cls.server_process = None

    def setUp(self):
        """Setup before each test."""
        edge_options = webdriver.EdgeOptions()
        edge_options.add_argument('--headless')
        edge_options.add_argument('--no-sandbox')
        edge_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Edge(
            service=Service(EdgeChromiumDriverManager().install()),
            options=edge_options
        )
        self.driver.implicitly_wait(10)

    def tearDown(self):
        """Cleanup after each test."""
        if hasattr(self, 'driver'):
            self.driver.quit()

    def test_login(self):
        """Test login functionality."""
        print("Testing login functionality...")
        driver = self.driver
        driver.get(f"{self.base_url}/login")
        print("Waiting for login form to load...")
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        password_input = driver.find_element(By.NAME, "password")
        print("Entering login credentials...")
        email_input.send_keys("ra@ra.com")
        password_input.send_keys("ra123")
        print("Clicking login button...")
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        print("Verifying login result...")
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dashboard"))
            )
            print("Login successful!")
            self.assertTrue(True, "Login successful")
        except Exception as e:
            print(f"Login failed: {e}")
            self.fail("Login failed")

    def test_add_transaction(self):
        """Test adding a transaction."""
        print("Testing add transaction...")
        self.test_login()
        driver = self.driver
        print("Navigating to add transaction page...")
        driver.get(f"{self.base_url}/add_transaction")
        print("Filling transaction form...")
        amount_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "amount"))
        )
        amount_input.send_keys("100.50")
        type_select = driver.find_element(By.NAME, "type")
        type_select.send_keys("debit")
        category_select = driver.find_element(By.NAME, "category")
        category_select.send_keys("Groceries")
        description_input = driver.find_element(By.NAME, "description")
        description_input.send_keys("Test transaction")
        print("Submitting transaction form...")
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()
        print("Verifying transaction addition result...")
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
            )
            print("Transaction added successfully!")
            self.assertTrue(True, "Transaction added successfully")
        except Exception as e:
            print(f"Transaction addition failed: {e}")
            self.fail("Transaction addition failed")

if __name__ == "__main__":
    unittest.main()
