
#%%%

# cd C:\Users\Pc\Desktop\Python\ps\Athyna\Recruit\Linkedin\
# streamlit run C:\Users\Pc\Desktop\Python\ps\Athyna\Recruit\Linkedin\Linkedin_Stream.py

import pandas as pd
import requests
import uuid
import re
from concurrent import futures
from threading import Lock
import time
import yaml
from yaml.loader import SafeLoader
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
from bs4 import BeautifulSoup
import re
import streamlit as st
import random
#import undetected_chromedriver as uc


class LinkedInBot:
    def __init__(self):
        #st.image(r'Logo.png')
        st.write(""" # Hello Sales team!
            Hope you guys have a great day! :-)

            Let's do a bit of magic. Shall we? 😁
                 """)
        self.messages_sent = 0
        self.profiles_liked = 0
        self.random_time = random.uniform(7.5, 11.5)
        self.final_profile_links = []

    def scroll_profile(self):
        # Scroll down slowly
        for _ in range(3):
            self.driver.execute_script("window.scrollBy(0, 200);")
            time.sleep(random.uniform(0.5, 1.5))

        # Scroll up slowly
        for _ in range(3):
            self.driver.execute_script("window.scrollBy(0, -300);")
            time.sleep(random.uniform(0.5, 1.5))

    def perform_human_actions(self):
        # Move the mouse randomly
        actions = ActionChains(self.driver)
        actions.move_by_offset(random.randint(-100, 100), random.randint(-100, 100))
        actions.perform()
        time.sleep(random.uniform(0.5, 1.5))

        # Scroll the page slightly
        self.driver.execute_script("window.scrollBy(0, {});".format(random.randint(-50, 50)))
        time.sleep(random.uniform(0.5, 1.5))

        # Press arrow keys randomly
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ARROW_DOWN)
        actions.send_keys(Keys.ARROW_UP)
        actions.perform()
        time.sleep(random.uniform(0.5, 1.5))


    def login(self):
        with st.form(key="my_form"):
            user_input = st.text_input("Username", help="Here you put your Linkedin email.")
            pass_input = st.text_input("Password", type="password", help="Here you put your Linkedin password.")
            message_input = st.text_input("Message", value="Hi, I came across your profile and thought it would be valuable for us to connect. Looking forward to networking with you. Best regards,", help="Here you put the message you wanna send. You gotta send something, cannot be empty. You can delete this paragraph as it was set as an example.")
            start_page = st.number_input("Start Page", min_value=1, value=1, step=1, help="This is the starting page of the linkedin bot when looking for results")
            end_page = st.number_input("End Page", min_value=1, value=100, step=1, help="This is the last page the linkedin bot will go over")
            submitted = st.form_submit_button("Login")
        st.write(
            """
            Team,

            Just remember that it is strongly recommended to iterate over 3 pages, e.g., 5 to 8.
            Also, ensure that you allow the page to fully render (show all components) after you log in.
            See the screenshot below. 

            Then make an ALT + TAB. This will allow it to run in the background
            so you do not have to stare at it until it finishes.

            Have fun!
            """
        )
        st.image(r'Screenshot 2024-04-30 202932.png')

        if submitted:
            #self.driver = uc.Chrome()
            options = Options()
            options.add_argument("--headless")  # Run Chrome in headless mode.
            options.add_argument("--no-sandbox")  # Bypass OS security model.
            options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems.
            options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration.
            options.add_argument("--remote-debugging-port=9222")  # This is important.
            self.driver = webdriver.Chrome(options=options)
            self.driver.get("https://www.linkedin.com/login/es?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")

            username_field = self.driver.find_element(By.XPATH, "//input[@name='session_key']")
            password_field = self.driver.find_element(By.XPATH, "//input[@name='session_password']")

            username_field.send_keys(user_input)
            password_field.send_keys(pass_input)
            time.sleep(self.random_time)

            sign_in_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            sign_in_button.click()
            time.sleep(self.random_time)
            self.search_and_connect(int(start_page), int(end_page), message_input)

    def search_and_connect(self, start_page, end_page, message_input):
        for page in range(start_page, end_page + 1):
            self.driver.get(f"https://www.linkedin.com/search/results/people/?geoUrn=%5B%22103644278%22%5D&keywords=ceo%20or%20director&network=%5B%22S%22%2C%22O%22%5D&origin=FACETED_SEARCH&page={page}&sid=1qH")
            total_height = self.driver.execute_script("return document.body.scrollHeight")
            for i in range(0, total_height, 200):
                self.driver.execute_script(f"window.scrollTo(0, {i});")
                time.sleep(random.uniform(0.5, 1.5))

            # Scroll back to the top
            self.driver.execute_script("window.scrollTo(0, 0);")

            everything_soup = BeautifulSoup(self.driver.page_source, "html.parser")
            time.sleep(self.random_time)
            name_elements = everything_soup.find_all("a", class_="app-aware-link")
            name_elements_with_profile = [name_element for name_element in name_elements if "profile" in name_element.get_text().lower()]
            matching_names = re.findall(r'Invite (.*?)to connect', (str(everything_soup)))
            processed_names = [name.rsplit(' ', 1)[0] for name in matching_names]
            st.write(processed_names)
            soup = BeautifulSoup(str(name_elements_with_profile), 'html.parser')
            final_list = []
            for a_tag in soup.find_all('a', class_="app-aware-link"):
                a_text = a_tag.get_text(strip=True)
                if any(name in a_text for name in processed_names):
                    final_list.append(a_tag)

            profile_links = [name_element["href"] for name_element in final_list if name_element.has_attr("href")]
            self.final_profile_links.extend(profile_links)
            time.sleep(self.random_time)

        for i in range(0, len(self.final_profile_links)):
            self.driver.get(self.final_profile_links[i])
            time.sleep(self.random_time)
            self.scroll_profile()
            #self.perform_human_actions()
            time.sleep(self.random_time)
            button = self.driver.find_element(By.XPATH, '//button[contains(@class, "artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action")]').click()
            time.sleep(self.random_time)
            time.sleep(4)
            add_note = self.driver.find_element(By.XPATH, "//button[@aria-label='Add a note']").click()
            time.sleep(self.random_time)
            send_message = self.driver.find_element(By.XPATH, "//*[@id='custom-message']")
            send_message.send_keys(f"{message_input}")
            time.sleep(self.random_time)
            success_message_button = self.driver.find_element(By.XPATH, '//button[contains(@aria-label, "Send")]').click()
            self.messages_sent += 1
            time.sleep(self.random_time)
            try:
                Dismiss_buttons = self.driver.find_element(By.XPATH, '//button[contains(@class, "ember-view artdeco-modal__dismiss")]')
                if Dismiss_buttons:
                    Dismiss_buttons.click()
                    time.sleep(self.random_time)
                time.sleep(self.random_time)
            except NoSuchElementException:
                pass
            time.sleep(self.random_time)
            Activity_buttons = self.driver.find_element(By.XPATH, '//a[contains(@class, "app-aware-link  profile-creator-shared-content-view__footer-action artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--3 artdeco-button--fluid artdeco-button--tertiary")]').click()
            time.sleep(self.random_time)
            try:
                Like_buttons = self.driver.find_element(By.XPATH, '//button[contains(@aria-label, "React Like")]').click()
                self.profiles_liked += 1
                time.sleep(self.random_time)
            except NoSuchElementException:
                pass
        time.sleep(self.random_time)

        st.write(f"Messages sent: {self.messages_sent}")
        st.write(f"Profiles liked: {self.profiles_liked}")

if __name__ == "__main__":
    bot = LinkedInBot()
    bot.login()
