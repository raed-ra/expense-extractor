#./tests/selenium/test_report_selenium.py

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def test_report_page_selenium():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 10)

    try:
        # Step 1: Go to login page
        driver.get("http://127.0.0.1:5000/auth/login")

        # Step 2: Log in
        wait.until(EC.presence_of_element_located((By.NAME, "email")))
        driver.find_element(By.NAME, "email").send_keys("test@example.com")
        driver.find_element(By.NAME, "password").send_keys("test123")
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()

        # Step 3: Go directly to /report
        driver.get("http://127.0.0.1:5000/report")

        # Step 4: Wait until something known exists (hacky but reliable fallback)
        wait.until(lambda d: "Transactions" in d.page_source or "report" in d.title.lower())

        # Step 5: Assert something minimal
        assert "Transactions" in driver.page_source or "report" in driver.title.lower()

    finally:
        driver.quit()

