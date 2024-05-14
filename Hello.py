import os
import shutil
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

def login(driver_path, browser):
    if browser == "chrome":
        options = ChromeOptions()
        service = ChromeService(executable_path=driver_path)
    elif browser == "edge":
        options = EdgeOptions()
        service = EdgeService(executable_path=driver_path)

    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    # options.add_argument("--headless")  # Uncomment if you need headless mode

    if browser == "chrome":
        driver = webdriver.Chrome(service=service, options=options)
    elif browser == "edge":
        driver = webdriver.Edge(service=service, options=options)

    driver.get("https://www.google.com")
    st.write(driver.title)  # Display the title of the page
    driver.quit()

if __name__ == "__main__":
    # Check for the presence of Google Chrome/ChromeDriver and Edge/EdgeDriver
    chrome_path = shutil.which("google-chrome")
    chrome_driver_path = shutil.which("chromedriver")
    edge_path = shutil.which("microsoft-edge")
    edge_driver_path = shutil.which("msedgedriver")
    
    st.write(f"Chrome path: {chrome_path}")
    st.write(f"ChromeDriver path: {chrome_driver_path}")
    st.write(f"Edge path: {edge_path}")
    st.write(f"EdgeDriver path: {edge_driver_path}")

    if chrome_path is None or chrome_driver_path is None:
        if edge_path is None or edge_driver_path is None:
            st.error("Neither Google Chrome/ChromeDriver nor Edge/EdgeDriver is installed.")
            st.stop()
        else:
            st.write("Using Edge/EdgeDriver.")
            browser = "edge"
            driver_path = edge_driver_path
    else:
        st.write("Using Chrome/ChromeDriver.")
        browser = "chrome"
        driver_path = chrome_driver_path
    
    with st.form(key="my_form"):
        user_input = st.text_input("Username", help="Here you put your LinkedIn email.")
        pass_input = st.text_input("Password", type="password", help="Here you put your LinkedIn password.")
        message_input = st.text_input("Message", value="Excited to connect! Hiring top talent in the USA within budget can be tough. At Athyna, we've got a proven strategy. By tapping into global talent pools, we deliver skilled professionals without the hefty costs. In just 5 to 7 days, we can introduce you to top-tier candidates across various roles. Ready to explore this opportunity?")
        start_page = st.number_input("Start Page", min_value=1, value=1, step=1, help="This is the starting page of the LinkedIn bot when looking for results")
        end_page = st.number_input("End Page", min_value=1, value=100, step=1, help="This is the last page the LinkedIn bot will go over")
        submitted = st.form_submit_button("Login")

    if submitted:
        os.environ['PATH'] += f":{os.path.dirname(driver_path)}"
        login(driver_path, browser)
        st.success("Driver executed successfully.")
