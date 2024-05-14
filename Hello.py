import os
import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
from zipfile import ZipFile

def download_chromedriver(driver_dir):
    # ChromeDriver download URL for the latest version compatible with Chrome 124
    download_url = "https://chromedriver.storage.googleapis.com/124.0.6367.0/chromedriver_linux64.zip"
    
    # Create driver directory if it doesn't exist
    if not os.path.exists(driver_dir):
        os.makedirs(driver_dir)

    # Download the ChromeDriver zip file
    zip_path = os.path.join(driver_dir, 'chromedriver.zip')
    with open(zip_path, 'wb') as file:
        response = requests.get(download_url)
        file.write(response.content)

    # Extract the zip file
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(driver_dir)

    # Remove the zip file
    os.remove(zip_path)

    # Return the path to the chromedriver executable
    return os.path.join(driver_dir, 'chromedriver')

def login(driver_path):
    options = Options()
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    # options.add_argument("--headless")  # Uncomment if you need headless mode

    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.google.com")
    st.write(driver.title)  # Display the title of the page
    driver.quit()

if __name__ == "__main__":
    with st.form(key="my_form"):
        user_input = st.text_input("Username", help="Here you put your LinkedIn email.")
        pass_input = st.text_input("Password", type="password", help="Here you put your LinkedIn password.")
        message_input = st.text_input("Message", value="Excited to connect! Hiring top talent in the USA within budget can be tough. At Athyna, we've got a proven strategy. By tapping into global talent pools, we deliver skilled professionals without the hefty costs. In just 5 to 7 days, we can introduce you to top-tier candidates across various roles. Ready to explore this opportunity?")
        start_page = st.number_input("Start Page", min_value=1, value=1, step=1, help="This is the starting page of the LinkedIn bot when looking for results")
        end_page = st.number_input("End Page", min_value=1, value=100, step=1, help="This is the last page the LinkedIn bot will go over")
        driver_dir = "/tmp/chromedriver"  # Directory to store ChromeDriver
        driver_path = os.path.join(driver_dir, 'chromedriver')
        submitted = st.form_submit_button("Login")

    if submitted:
        if not os.path.isfile(driver_path):
            st.write("Downloading ChromeDriver...")
            driver_path = download_chromedriver(driver_dir)
        login(driver_path)
        st.success("Driver executed successfully.")
