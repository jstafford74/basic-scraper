import math
import time
from typing import List

from application import Application
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from sites import workday_data
from utils import (
    find_elements_by_xpath,
    get_active_and_inactive_apps,
    write_objects_to_csv,
)


class WorkdaySite:
    def __init__(self, name, url, email, password):
        self.name = name
        self.url = url
        self.email = email
        self.password = password
    

workday_list = [WorkdaySite(**data) for data in workday_data]

parent_tabpanel_div = "//div[@role='tabpanel' and not(@hidden)]"
    
def workday_scrape(sites_list:List[WorkdaySite]):
    # Load environment variables
    load_dotenv()
    for site in sites_list:
        applications = []

        # Options for browser to remain open
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--log-level=1")
        # Define and locate chrome driver/service
        service = Service(
            r"C:\Users\jstaf\Documents\chromedriver\chromedriver-win64\chromedriver.exe"
        )
        browser = webdriver.Chrome(service=service, options=chrome_options)

        print(site.name)
        print(site.url)
        is_webpage = "/login" in site.url
        email_field_id = "input-4"
        password_field_id = "input-5"

        browser.get(site.url)
         # pause for username & password entry
        time.sleep(3)

        # ===============LOGIN===============
        try:
            if is_webpage:
                # Find the elements
                email_element = browser.find_element(By.ID, email_field_id)
                password_element = browser.find_element(By.ID, password_field_id)
                sign_in_button = browser.find_element(By.CLASS_NAME, "css-1s1r74k")

                # Enter username
                email_element.click()
                email_element.clear()
                email_element.send_keys(site.email)
                time.sleep(2)
                # enter password
                password_element.click()
                password_element.clear()
                password_element.send_keys(site.password)
                time.sleep(2)
                # Login
                sign_in_button.click()
                time.sleep(10)
                print("logged in")

                # Find account settings button for signout
                # account_button = browser.find_element(By.ID, "accountSettingsButton")
                # #Find Active & Inactive Tabs
  
                status_tabs = find_elements_by_xpath(browser,"//section[@data-automation-id='applicationsSectionHeading']//button[@role='tab']")
                active_button_text = status_tabs[0].text if status_tabs[0] else None
                # inactive_button_text = status_tabs[1].text if status_tabs[1] else None

                active_apps = get_active_and_inactive_apps(active_button_text)

                # inactive_apps = get_active_and_inactive_apps(inactive_button_text)
                
                upper_limit = math.ceil(int(active_apps) / 4)
                # Loop through all active tabs based on 4 displayed
                for i in range(1, upper_limit + 1):
                    print(f"iteration: {i}")
                    time.sleep(3)
                    job_title_column = find_elements_by_xpath(browser,f"{parent_tabpanel_div}//div[@data-automation-id='applicationTitle']")
                    job_req_column = find_elements_by_xpath(browser,f"{parent_tabpanel_div}//td[@class='css-x4yhc3']")
                    status_column = find_elements_by_xpath(browser,f"{parent_tabpanel_div}//div[@data-automation-id='applicationStatus']")
                    date_submitted_column = find_elements_by_xpath(browser,f"{parent_tabpanel_div}//td[@class='css-62prxo']")

                    for idx,row in enumerate(job_title_column):
                        job_title = row.text
                        job_req_id = job_req_column[idx].text
                        job_status = status_column[idx].text
                        date_submitted=date_submitted_column[idx].text

                        job_app = Application(site.name,job_title,job_req_id,job_status,date_submitted,is_active=True)

                        applications.append(job_app)

                    time.sleep(3)

                    print("=====Checking for Pagination=====")
                    has_pagination = find_elements_by_xpath(browser,f"{parent_tabpanel_div}//nav[@data-automation-id='pagination']")

                    if not has_pagination:
                        print("no pagination present")
                    else:
                        print(f"{site.name} pagination: {has_pagination[0]}")
                        next_button = browser.find_element(By.XPATH,f"{parent_tabpanel_div}//nav[@data-automation-id='pagination']//button[@aria-label='Next' and not(@aria-disabled='True')]") if len(has_pagination) else False
                        print("Clicking Next Button")
                        next_button.click()
                        time.sleep(3)
                                            
                # Click on the drop down
                # account_button.click()
                # time.sleep(5)
                # Find the Sign Out Button
                # sign_out_button = browser.find_element(By.ID, "item1")
                # Performing the mouse hover action on the target element.
                # print("Active Button")
                # print_element(active_button)
                # print(len(active_button))


                print(f"Applications: {len(applications)}")
                print(applications)
                write_objects_to_csv('current_applications.csv',applications)
                # sign_out_button.click()
                time.sleep(10)

        except Exception:
            print("Something went wrong")
            print(Exception)
        finally:
            print("logged in")

        # # ===============LOGOUT===============
        # try:
        #     if is_webpage:
        #         # Find the elements
        #         account_button = browser.find_element(By.ID, "accountSettingsButton")

        #         # Click on the drop down
        #         account_button.click()
        #         time.sleep(2)
        #         # Find the Sign Out Button
        #         sign_out_button = browser.find_element(By.ID, "item1")
        #         sign_out_button.click()
        # except Exception:
        #     print("Something went wrong")
        #     print(Exception)
        # finally:
        #     print("logged out")

        # try:
        #     time.sleep(5)
        #     button_elements = browser.find_elements(By.TAG_NAME, "button")
        #     submit_button = None
        #     for button in button_elements:
        #         if button.text == "Search for Jobs":
        #             submit_button = button
        #             continue

        #     time.sleep(2)
        #     submit_button.click()
        # finally:
        #     print("clicked on search tab")

        # try:
        #     time.sleep(5)

        #     filter_button_elements = browser.find_elements(By.TAG_NAME, "button")
        #     location_button = None

        #     for button in filter_button_elements:
        #         if button.text == "Distance or Location":
        #             location_button = button
        #             continue

        #     time.sleep(1)
        #     location_button.click()

        # finally:
        #     print("clicked on location selection")

        # try:
        #     time.sleep(2)
        #     location_checkbox = browser.find_element(By.ID, "location")

        #     location_checkbox.click()
        #     time.sleep(3)
        #     location_container = browser.find_element(
        #         By.CLASS_NAME, "ReactVirtualized__Grid__innerScrollContainer"
        #     )

        #     first_checkbox = location_container.find_elements(By.TAG_NAME, "input")
        #     # second_checkbox = location_container.find_element(
        #     #     By.XPATH, ".//*[contains(text(), 'USA, CT, Remote')]"
        #     # )
        #     print(first_checkbox)
        #     print(len(first_checkbox))
        #     for _ in range(1):
        #         actions.move_to_element(location_container).perform()
        #         print(first_checkbox)
        #         print(len(first_checkbox))

        #     # for checkbox in first_checkbox:
        #     #     print(
        #     #         f"{checkbox.accessible_name}: {re.search('USA, CT, Remote', checkbox.accessible_name)}"
        #     #     )
        #     #     if checkbox.accessible_name == "USA, CT, Remote":
        #     #         print("checkbox")
        #     #         print(checkbox)
        #     #         checkbox.click()

        # finally:
        # print("clicked on location")


workday_scrape(workday_list)


# "View Jobs"
# ""
