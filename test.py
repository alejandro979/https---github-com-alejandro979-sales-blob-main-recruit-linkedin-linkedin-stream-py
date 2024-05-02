from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def login():
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode.
    options.add_argument("--no-sandbox")  # Bypass OS security model.
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems.
    options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration.
    options.add_argument("--remote-debugging-port=9222")  # This is important.
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get("https://www.google.com")  # Replace with your target URL

if __name__ == "__main__":
    login()

