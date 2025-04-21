import csv
import os
import re
import time
from datetime import datetime
from typing import List, Union

from bson import ObjectId
from constants import (
    EMAIL_FIELD_ID,
    PASSWORD_FIELD_ID,
    SIGN_IN_CLASS,
    SIGN_OUT_BUTTON,
    STATUS_TABS_SECTION,
    UTILITY_BUTTON,
)
from controllers import ApplicationStatusController
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def print_element(element):
    print("==============Printing Element==============")
    print(element)
    print(
        "Element Text:", element.text
    )  # Prints the visible text of the element [1, 2, 8]
    print("Element Tag Name:", element.tag_name)  # Prints the HTML tag name
    print("Element ID:", element.get_attribute("id"))  # Prints the "id" attribute value
    print(
        "Element Class Name:", element.get_attribute("class")
    )  # Prints the "class" attribute value


def get_active_and_inactive_apps(string):
    x = string.split("(")
    x = x[1].split(")")
    x = x[0]
    return x


def find_elements_by_xpath(
    driver: WebDriver, xpath: str
) -> Union[bool, List[WebElement]]:
    try:
        elements = driver.find_elements(By.XPATH, xpath)
        # Return elements if found, else return False
        return elements if elements else False
    except NoSuchElementException:
        return False


def find_element_by_xpath(
    driver: WebDriver, xpath: str
) -> Union[bool, List[WebElement]]:
    try:
        element = driver.find_element(By.XPATH, xpath)
        # Return elements if found, else return False
        return element if element else False
    except NoSuchElementException:
        return False


def write_objects_to_csv(file_name: str, objects: list):
    if not objects:
        print("No data to write to CSV")
        return

    # Convert objects to dictionaries
    objects_dict = [obj.to_dict() for obj in objects]

    # Check if the file already exists
    file_exists = os.path.isfile(file_name)

    with open(file_name, mode="a", newline="", encoding="utf-8") as file:
        # Create a writer object
        writer = csv.DictWriter(file, fieldnames=objects_dict[0].keys())

        # If the file doesn't exist, write the header row
        if not file_exists:
            writer.writeheader()

        # Write the data rows
        writer.writerows(objects_dict)

    print(f"Data written to {file_name} successfully.")


def instantiate_browser():
    # Options for browser to remain open
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    # Define and locate chrome driver/service
    service = Service(
        r"C:\Users\jstaf\Documents\chromedriver\chromedriver-win64\chromedriver.exe"
    )
    browser = webdriver.Chrome(service=service, options=chrome_options)

    return browser


def extract_integer(s):
    # Search for an integer pattern in the string
    match = re.search(r"\d+", s)
    # Return the integer if found, else return None
    return int(match.group()) if match else None


def login(browser, site):
    # Find the log in elements
    email_element = browser.find_element(By.ID, EMAIL_FIELD_ID)
    password_element = browser.find_element(By.ID, PASSWORD_FIELD_ID)
    sign_in_button = browser.find_element(By.CLASS_NAME, SIGN_IN_CLASS)
    # Enter username
    email_element.click()
    email_element.clear()
    email_element.send_keys(site["email"])
    time.sleep(1)
    # enter password
    password_element.click()
    password_element.clear()
    password_element.send_keys(site["password"])
    time.sleep(1)
    # Login
    sign_in_button.click()
    time.sleep(4)
    print("logged in")


def logout(browser):
    # Click on account settings
    account_button = find_element_by_xpath(browser, UTILITY_BUTTON)
    time.sleep(3)
    if account_button:
        account_button.click()
    time.sleep(3)
    # Find the Sign Out Button
    sign_out_button = find_element_by_xpath(browser, SIGN_OUT_BUTTON)
    time.sleep(2)
    if sign_out_button:
        sign_out_button.click()
    time.sleep(2)
    browser.close()


def find_active_and_inactive_tabs(browser, site):
    now = datetime.now()
    dt_string = now.strftime("%m-%d-%Y")
    company_id = ObjectId(site["_id"])
    application_status_controller = ApplicationStatusController()
    print("find_active_and_inactive_tabs")
    print(site)
    status_tabs = find_elements_by_xpath(browser, STATUS_TABS_SECTION)

    active_button_text = (
        status_tabs[0].text if status_tabs and len(status_tabs) else None
    )
    inactive_button_text = (
        status_tabs[1].text if status_tabs and len(status_tabs) else None
    )

    active_apps = extract_integer(active_button_text) if active_button_text else 0
    inactive_apps = extract_integer(inactive_button_text) if inactive_button_text else 0

    current_app_status = application_status_controller.find_one_document(
        {"measure_date": dt_string}
    )

    is_upsert = True if current_app_status is None else False

    if active_apps > 0:
        active_apps_update = application_status_controller.update_one_document(
            {
                "measure_date": dt_string,
                "active_companies": {"$nin": [ObjectId(company_id)]},
            },
            {
                "$inc": {"active": active_apps},
                "$push": {"active_companies": ObjectId(company_id)},
            },
            upsert=is_upsert,
        )
        if active_apps_update.modified_count > 0:
            print(f"{site['name']} active apps updated successfully.")
        else:
            print("No document found or document was not modified.")

    if inactive_apps > 0:
        inactive_apps_update = application_status_controller.update_one_document(
            {
                "measure_date": dt_string,
                "inactive_companies": {"$nin": [ObjectId(company_id)]},
            },
            {
                "$inc": {"inactive": inactive_apps},
                "$push": {"inactive_companies": ObjectId(company_id)},
            },
            upsert=is_upsert,
        )
        if inactive_apps_update.modified_count > 0:
            print(f"{site['name']} inactive apps updated successfully.")
        else:
            print("No document found or document was not modified.")

    return [active_apps, inactive_apps, status_tabs]
