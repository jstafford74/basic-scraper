import csv
import os
from typing import List, Union

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def print_element(element):
    print("==============Printing Element==============")
    print(element)
    print("Element Text:", element.text)  # Prints the visible text of the element [1, 2, 8]
    print("Element Tag Name:", element.tag_name) # Prints the HTML tag name
    print("Element ID:", element.get_attribute("id"))  # Prints the "id" attribute value
    print("Element Class Name:", element.get_attribute("class"))  # Prints the "class" attribute value

def get_active_and_inactive_apps(string):
    x = string.split("(")
    x = x[1].split(")")
    x = x[0]
    return x

def find_elements_by_xpath(driver: WebDriver, xpath: str) -> Union[bool, List[WebElement]]:
    try:
        elements = driver.find_elements(By.XPATH, xpath)
        # Return elements if found, else return False
        return elements if elements else False
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

    with open(file_name, mode='a', newline='', encoding='utf-8') as file:
        # Create a writer object
        writer = csv.DictWriter(file, fieldnames=objects_dict[0].keys())

        # If the file doesn't exist, write the header row
        if not file_exists:
            writer.writeheader()

        # Write the data rows
        writer.writerows(objects_dict)
        
    print(f"Data written to {file_name} successfully.")