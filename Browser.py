import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
load_dotenv()
service = Service(r"C:\Users\jstaf\Documents\chromedriver\chromedriver.exe")
browser = webdriver.Chrome(service=service, options=chrome_options)
firefox_service = Service(r"C:\Users\jstaf\Documents\geckodriver\geckodriver.exe")
browser.get("https://www.dice.com/dashboard/login")
DICE_USERNAME = os.getenv("DICE_USERNAME")
DICE_PASSWORD = os.getenv("DICE_PASSWORD")
time.sleep(3)
# elem = browser.find_element(By.NAME, "email")

try:
    email_element = browser.find_element(By.NAME, "email")
    continue_button = browser.find_element(By.TAG_NAME, "button")
    email_element.click()
    email_element.clear()
    email_element.send_keys(DICE_USERNAME)
    time.sleep(3)
    continue_button.click()

    time.sleep(3)
finally:
    print("email entered")

try:
    password_element = browser.find_element(By.NAME, "password")
    buttons = browser.find_elements(By.TAG_NAME, "button")
    password_element.click()
    password_element.clear()
    password_element.send_keys(DICE_PASSWORD)
    time.sleep(3)
    submit_button = buttons[1]
    # print(buttons)
    submit_button.click()

    time.sleep(3)
finally:
    print("password entered")

    # Find the search box
# input = browser.locate_with(By.TAG_NAME, "input")
# email_input = browser.find_element(By.XPATH, "//form[input/@name='email']")
