import math
import time
from typing import List

from application import Application
from constants import (
    ACCOUNT_SETTINGS_ID,
    DATE_SUBMITTED_COLUMN,
    EMAIL_FIELD_ID,
    JOB_REQ_COLUMN,
    JOB_STATUS_COLUMN,
    JOB_TITLE_COLUMN,
    NEXT_BUTTON,
    PAGINATION_NAV,
    PARENT_TABPANEL_DIV,
    PASSWORD_FIELD_ID,
    SIGN_IN_CLASS,
)
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

        browser.get(site.url)
         # pause for username & password entry
        time.sleep(2)

        # ===============LOGIN===============
        try:
            if is_webpage:
                # Find the elements
                email_element = browser.find_element(By.ID, EMAIL_FIELD_ID)
                password_element = browser.find_element(By.ID, PASSWORD_FIELD_ID)
                sign_in_button = browser.find_element(By.CLASS_NAME,SIGN_IN_CLASS )

                # Enter username
                email_element.click()
                email_element.clear()
                email_element.send_keys(site.email)
                time.sleep(1)
                # enter password
                password_element.click()
                password_element.clear()
                password_element.send_keys(site.password)
                time.sleep(1)
                # Login
                sign_in_button.click()
                time.sleep(4)
                print("logged in")

                # Find account settings button for signout
                account_button = browser.find_element(By.ID, ACCOUNT_SETTINGS_ID)
                
                #Find Active & Inactive Tabs
                status_tabs = find_elements_by_xpath(browser,"//section[@data-automation-id='applicationsSectionHeading']//button[@role='tab']")
                active_button_text = status_tabs[0].text if status_tabs[0] else None
                inactive_button_text = status_tabs[1].text if status_tabs[1] else None

                active_apps = get_active_and_inactive_apps(active_button_text)
                inactive_apps = get_active_and_inactive_apps(inactive_button_text)
                
                active_app_upper_limit = math.ceil(int(active_apps) / 4)
                inactive_app_upper_limit = math.ceil(int(inactive_apps) / 4)

                # If zero apps are active or inactive report them per employer
                if int(active_apps) == 0:
                    job_app = Application(site.name,"N/A", "N/A", "N/A", "N/A", is_active=True)
                    applications.append(job_app)
                    
                if int(inactive_apps) == 0:
                    job_app = Application(site.name,"N/A", "N/A", "N/A", "N/A", is_active=False)
                    applications.append(job_app)

                # If both app types are equal to zero, continue to next employer
                if int(active_apps) == 0 and int(inactive_apps) == 0:
                    print("both active and inactive apps are zero")
                    zero_active_job_app = Application(site.name,"N/A", "N/A", "N/A", "N/A", is_active=True)
                    zero_inactive_job_app = Application(site.name,"N/A", "N/A", "N/A", "N/A", is_active=False)
                    applications.append(zero_active_job_app,zero_inactive_job_app)
                    write_objects_to_csv('current_applications.csv',applications)
                    continue     

                #//START active tab iteration
                for i in range(1, active_app_upper_limit + 1):
                    print(f"iteration: {i}")
                    time.sleep(2)
                    job_title_column = find_elements_by_xpath(browser,f"//{PARENT_TABPANEL_DIV}//{JOB_TITLE_COLUMN}")
                    job_req_column = find_elements_by_xpath(browser,f"//{PARENT_TABPANEL_DIV}//{JOB_REQ_COLUMN}")
                    status_column = find_elements_by_xpath(browser,f"//{PARENT_TABPANEL_DIV}//{JOB_STATUS_COLUMN}")
                    date_submitted_column = find_elements_by_xpath(browser,f"//{PARENT_TABPANEL_DIV}//{DATE_SUBMITTED_COLUMN}")

                    for idx,row in enumerate(job_title_column):
                        job_title = row.text
                        job_req_id = job_req_column[idx].text
                        job_status = status_column[idx].text
                        date_submitted=date_submitted_column[idx].text

                        job_app = Application(site.name,job_title,job_req_id,job_status,date_submitted,is_active=True)

                        applications.append(job_app)

                    time.sleep(2)

                    print("=====Checking for Pagination=====")
                    has_pagination = find_elements_by_xpath(browser,f"//{PARENT_TABPANEL_DIV}//{PAGINATION_NAV}")

                    if not has_pagination:
                        print("no pagination present")
                    else:
                        print(f"{site.name} pagination: {has_pagination[0]}")
                        next_button = browser.find_element(By.XPATH,f"//{PARENT_TABPANEL_DIV}//{PAGINATION_NAV}//{NEXT_BUTTON}") if len(has_pagination) else False
                        print("Clicking Next Button")
                        next_button.click()
                        time.sleep(3)
                #//END active tab iteration
                
                #//START inactive tab iteration
                status_tabs[1].click()
                if int(inactive_apps) > 0:
                    for i in range(1, inactive_app_upper_limit + 1):
                        print(f"inactive iteration: {i}")
                        time.sleep(2)
                        inactive_job_title_column = find_elements_by_xpath(browser,f"//{PARENT_TABPANEL_DIV}//{JOB_TITLE_COLUMN}")
                        inactive_job_req_column = find_elements_by_xpath(browser,f"//{PARENT_TABPANEL_DIV}//{JOB_REQ_COLUMN}")
                        inactive_status_column = find_elements_by_xpath(browser,f"//{PARENT_TABPANEL_DIV}//{JOB_STATUS_COLUMN}")
                        inactive_date_submitted_column = find_elements_by_xpath(browser,f"//{PARENT_TABPANEL_DIV}//{DATE_SUBMITTED_COLUMN}")

                        for idx,row in enumerate(inactive_job_title_column):
                            job_title = row.text
                            job_req_id = inactive_job_req_column[idx].text
                            job_status = inactive_status_column[idx].text
                            date_submitted = inactive_date_submitted_column[idx].text

                            job_app = Application(site.name,job_title,job_req_id,job_status,date_submitted,is_active=False)

                            applications.append(job_app)

                        time.sleep(2)

                        print("=====Checking for inactive Pagination=====")
                        has_pagination = find_elements_by_xpath(browser,f"//{PARENT_TABPANEL_DIV}//{PAGINATION_NAV}")

                        if not has_pagination:
                            print("no pagination present")
                        else:
                            print(f"{site.name} pagination: {has_pagination[0]}")
                            next_button = browser.find_element(By.XPATH,f"//{PARENT_TABPANEL_DIV}//{PAGINATION_NAV}//{NEXT_BUTTON}") if len(has_pagination) else False
                            print("Clicking Next Button")
                            next_button.click()
                            time.sleep(2)
                #//END active tab iteration
                

                print(f"Applications: {len(applications)}")
                
                write_objects_to_csv('current_applications.csv',applications)
                # sign_out_button.click()
                time.sleep(2)

        except Exception:
            print("Something went wrong")
            print(Exception)
        finally:
            # Click on account settings
            account_button.click()
            time.sleep(3)
            # Find the Sign Out Button
            sign_out_button = browser.find_element(By.XPATH, "//button[@aria-label='Sign Out']")
            sign_out_button.click()
            time.sleep(2)
            browser.close()


workday_scrape(workday_list)
