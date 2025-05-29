# ./tests/selenium/test_upload_selenium.py

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_dummy_pdf(path):
    c = canvas.Canvas(path, pagesize=letter)
    c.drawString(100, 750, "This is a dummy test PDF for Selenium.")
    c.save()

def test_upload_page_selenium():
    print("🚀 Starting Selenium Test")

    test_dir = 'tests/test_files'
    os.makedirs(test_dir, exist_ok=True)
    test_pdf_path = os.path.abspath(os.path.join(test_dir, 'real_statement.pdf'))

    if not os.path.exists(test_pdf_path):
        print(f"⚠️ real_statement.pdf not found. Generating dummy PDF.")
        generate_dummy_pdf(test_pdf_path)
        is_temp_file = True
    else:
        print(f"✅ Using existing PDF: {test_pdf_path}")
        is_temp_file = False

    chromedriver_path = "/Users/raedr/.wdm/drivers/chromedriver/mac64/136.0.7103.94/chromedriver-mac-x64/chromedriver"

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)

    try:
        print("➡️ Navigating to login page...")
        driver.get('http://127.0.0.1:5000/auth/login')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'email'))
        )
        print("✅ Login form loaded.")

        driver.find_element(By.NAME, 'email').send_keys('testuser@example.com')
        driver.find_element(By.NAME, 'password').send_keys('password')
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        print("✅ Logged in successfully.")

        print("➡️ Navigating to upload page...")
        driver.get('http://127.0.0.1:5000/upload')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'pdf_file'))
        )
        print("✅ Upload form loaded.")

        upload_input = driver.find_element(By.NAME, 'pdf_file')
        submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        upload_input.send_keys(test_pdf_path)
        submit_button.click()
        print("✅ PDF file submitted.")

        print("⏳ Waiting for transactions table (post-reload)...")
        WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.ID, 'transactionsTable'))
        )
        print("✅ Transactions table rendered successfully. Test PASSED.")

    except Exception as e:
        print("❌ Test FAILED.")
        print("📄 Final page source snapshot:\n", driver.page_source[:1500])
        raise AssertionError("Expected parsed table not found.") from e

    finally:
        driver.quit()
        if is_temp_file and os.path.exists(test_pdf_path):
            os.remove(test_pdf_path)

if __name__ == "__main__":
    test_upload_page_selenium()
