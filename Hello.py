
import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def login(driver_path):
    options = Options()
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration

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
        driver_path = st.text_input("Path to Driver", help="Specify the path to the ChromeDriver or EdgeDriver executable.")
        submitted = st.form_submit_button("Login")

    if submitted:
        login(driver_path)
        st.success("Driver executed successfully.")

