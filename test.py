
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import streamlit as st

chromedriver_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Create a Service object with the path to the ChromeDriver executable
service = Service(chromedriver_path)

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(service=service)


user_input = st.text_input("Username", help="Here you put your Linkedin email.")
pass_input = st.text_input("Password", type="password", help="Here you put your Linkedin password.")
message_input = st.text_input("Message", value="Excited to connect! Hiring top talent in the USA within budget can be tough. At Athyna, we've got a proven strategy. By tapping into global talent pools, we deliver skilled professionals without the hefty costs. In just 5 to 7 days, we can introduce you to top-tier candidates across various roles. Ready to explore this opportunity?")
start_page = st.number_input("Start Page", min_value=1, value=1, step=1, help="This is the starting page of the linkedin bot when looking for results")
end_page = st.number_input("End Page", min_value=1, value=100, step=1, help="This is the last page the linkedin bot will go over")
submitted = st.form_submit_button("Login")
path = st.text_input("Path")

