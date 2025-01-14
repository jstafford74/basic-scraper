import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def workday_scrape(site):
    # Load environment variables
    load_dotenv()
    URL = os.getenv(f"{site}_URL")
    USERNAME = os.getenv(f"{site}_USERNAME")
    PASSWORD = os.getenv(f"{site}_PASSWORD")
    print(URL)
    print(USERNAME)
    # Options for browser to remain open
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    # Define and locate chrome driver/service
    service = Service(r"C:\Users\jstaf\Documents\chromedriver\chromedriver.exe")
    browser = webdriver.Chrome(service=service, options=chrome_options)

    is_webpage = "/login" in URL

    email_field_id = "input-4"
    password_field_id = "input-5"

    # firefox_service = Service(r"C:\Users\jstaf\Documents\geckodriver\geckodriver.exe")
    browser.get(URL)

    # pause for username & password entry
    time.sleep(3)
    # elem = browser.find_element(By.NAME, "email")

    try:
        if is_webpage:
            # Find the elements
            email_element = browser.find_element(By.ID, email_field_id)
            password_element = browser.find_element(By.ID, password_field_id)
            sign_in_button = browser.find_element(By.CLASS_NAME, "css-1s1r74k")
            # Enter username
            email_element.click()
            email_element.clear()
            email_element.send_keys(USERNAME)
            time.sleep(2)
            # enter password
            password_element.click()
            password_element.clear()
            password_element.send_keys(PASSWORD)
            time.sleep(2)
            # Login
            sign_in_button.click()

    except Exception:
        print("Something went wrong")
        print(Exception)
    finally:
        print("logged in")

    try:
        time.sleep(5)
        # button_elements = WebDriverWait(browser, 10).until(
        #     EC.presence_of_element_located(By.TAG_NAME, "button")
        # )
        button_elements = browser.find_elements(By.TAG_NAME, "button")
        submit_button = None
        for button in button_elements:
            if button.text == "Search for Jobs":
                submit_button = button
                continue

        time.sleep(2)
        submit_button.click()
    finally:
        print("clicked on search tab")

    try:
        time.sleep(5)
        # filter_button_elements = WebDriverWait(browser, 10).until(
        #     EC.presence_of_element_located((By.TAG_NAME, "button"))
        # )

        filter_button_elements = browser.find_elements(By.TAG_NAME, "button")
        location_button = None

        for button in filter_button_elements:
            if button.text == "Distance or Location":
                location_button = button
                continue

        time.sleep(1)
        location_button.click()

    finally:
        print("clicked on location selection")

    try:
        # location_checkbox = WebDriverWait(browser, 10).until(
        #     EC.presence_of_element_located((By.id, "location"))
        # )
        time.sleep(2)
        location_checkbox = browser.find_element(By.ID, "location")
        print(location_checkbox)
        location_checkbox.click()
    finally:
        print("clicked on location")


workday_scrape("WORKDAY")
