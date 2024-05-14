import os
import subprocess
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
from zipfile import ZipFile, BadZipFile

def install_chrome():
    # Add Google Chrome's repository and install it
    st.write("Adding Google Chrome repository and installing it...")
    subprocess.run("wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -", shell=True, check=True)
    subprocess.run('sh -c \'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list\'', shell=True, check=True)
    subprocess.run(["apt-get", "update"], check=True)
    subprocess.run(["apt-get", "install", "-y", "google-chrome-stable"], check=True)
    st.write("Google Chrome installed.")

def download_chromedriver(driver_dir):
    # ChromeDriver download URL for the latest version compatible with Chrome 114
    download_url = "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip"
    
    # Create driver directory if it doesn't exist
    if not os.path.exists(driver_dir):
        os.makedirs(driver_dir)

    # Download the ChromeDriver zip file
    zip_path = os.path.join(driver_dir, 'chromedriver.zip')
    st.write(f"Downloading ChromeDriver from {download_url}")
    response = requests.get(download_url)

    # Check if the response is valid
    if response.status_code != 200:
        st.error("Failed to download ChromeDriver.")
        return None

    with open(zip_path, 'wb') as file:
        file.write(response.content)

    # Verify if the downloaded file is a valid zip file
    try:
        with ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(driver_dir)
    except BadZipFile:
        st.error("The downloaded file is not a valid zip file.")
        return None

    # Remove the zip file
    os.remove(zip_path)

    # Check if chromedriver executable exists
    driver_path = os.path.join(driver_dir, 'chromedriver')
    if not os.path.isfile(driver_path):
        st.error("ChromeDriver executable not found after extraction.")
        return None

    # Return the path to the chromedriver executable
    return driver_path

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
    # Check if Google Chrome is installed, if not, install it
    chrome_path = "/usr/bin/google-chrome"
    if not os.path.exists(chrome_path):
        st.write("Installing Google Chrome...")
        install_chrome()
    
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
            if not driver_path:
                st.error("Failed to download or extract ChromeDriver.")
                st.stop()
        os.environ['PATH'] += f":{os.path.dirname(chrome_path)}"
        login(driver_path)
        st.success("Driver executed successfully.")
