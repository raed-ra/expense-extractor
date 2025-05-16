# ./tests/selenium/test_upload_selenium.py
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

def test_upload_page_selenium():
    driver = webdriver.Chrome()
    driver.get('http://localhost:5000/upload')

    upload_input = driver.find_element(By.NAME, 'pdf_file')
    submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

    test_pdf_path = os.path.abspath('tests/test_files/sample.pdf')
    upload_input.send_keys(test_pdf_path)
    submit_button.click()

    time.sleep(5)  # wait for processing (replace with explicit wait if needed)

    # Check for message or table
    assert "parsed results" in driver.page_source or "transactionsTable" in driver.page_source

    driver.quit()
