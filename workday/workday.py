import math
import time
import traceback
from typing import List

from application import Application, TotalJob
from constants import (
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
    SIGN_OUT_BUTTON,
    STATUS_TABS_SECTION,
    UTILITY_BUTTON,
)
from dotenv import load_dotenv
from search import (
    FOUND_JOBS,
    KEYWORD_SEARCH_BUTTON,
    KEYWORD_SEARCH_INPUT,
    SEARCH_FOR_JOBS,
)
from selenium.webdriver.common.by import By
from sites import workday_data
from utils import (
    extract_integer,
    find_element_by_xpath,
    find_elements_by_xpath,
    get_active_and_inactive_apps,
    instantiate_browser,
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
        total_jobs = []
        # Options for browser to remain open
        # chrome_options = Options()
        # chrome_options.add_experimental_option("detach", True)
        # chrome_options.add_argument("--log-level=1")
        # Define and locate chrome driver/service
        # service = Service(
        #     r"C:\Users\jstaf\Documents\chromedriver\chromedriver-win64\chromedriver.exe"
        # )
        # browser = webdriver.Chrome(service=service, options=chrome_options)
        browser = instantiate_browser()

        print(f"Visiting {site.name} at {site.url}")
        browser.get(site.url)
        # pause for username & password entry
        time.sleep(2)

        # ===============LOGIN===============
        try:
             # Find the log in elements
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

            #Find Active & Inactive Tabs
            
            status_tabs = find_elements_by_xpath(browser,STATUS_TABS_SECTION)
            print(f"STATUS TABS:{status_tabs}")
            active_button_text = status_tabs[0].text if status_tabs and len(status_tabs) else None
            inactive_button_text = status_tabs[1].text if status_tabs and len(status_tabs) else None
            
            active_apps = get_active_and_inactive_apps(active_button_text) if active_button_text else 0
            inactive_apps = get_active_and_inactive_apps(inactive_button_text) if inactive_button_text else 0
            print(f"active tabs:{active_apps}")
            print(f"iactive tabs:{inactive_apps}")

            active_app_upper_limit = math.ceil(int(active_apps) / 4) if active_apps else 0
            inactive_app_upper_limit = math.ceil(int(inactive_apps) / 4) if inactive_apps else 0

            # If zero apps are active or inactive report them per employer
            if int(active_apps) == 0:
                job_app = Application(site.name,"N/A", "N/A", "N/A", "N/A", is_active=True)
                applications.append(job_app)
                
            if int(inactive_apps) == 0:
                job_app = Application(site.name,"N/A", "N/A", "N/A", "N/A", is_active=False)
                applications.append(job_app)
           
            else:    
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
                        next_button = find_element_by_xpath(browser,f"//{PARENT_TABPANEL_DIV}//{PAGINATION_NAV}//{NEXT_BUTTON}") if len(has_pagination) else False
                        print("Clicking Next Button")
                        next_button.click()
                        time.sleep(2)
                #//END active tab iteration

                #//START inactive tab iteration
                if status_tabs and len(status_tabs):
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
                            next_button = find_element_by_xpath(browser,f"//{PARENT_TABPANEL_DIV}//{PAGINATION_NAV}//{NEXT_BUTTON}") if len(has_pagination) else False
                            print("Clicking Next Button")
                            next_button.click()
                            time.sleep(2)
                #//END active tab iteration
            
            print(f"Applications: {len(applications)}")
            
            write_objects_to_csv('current_applications.csv',applications)
            
            search_jobs = browser.find_element(By.XPATH,SEARCH_FOR_JOBS) if browser.find_element(By.XPATH,SEARCH_FOR_JOBS) else None
            
            if search_jobs:
                print("clicking on search for jobs")
                search_jobs.click()
                time.sleep(4)

                found_jobs = browser.find_element(By.XPATH,FOUND_JOBS)
                total_found_jobs = extract_integer(found_jobs.text)
                
                print(f"Total: {extract_integer(found_jobs.text)}")
                
                keyword_search = find_element_by_xpath(browser,KEYWORD_SEARCH_INPUT)
                
                if keyword_search:
                    keyword_search.click()
                    keyword_search.clear()
                    keyword_search.send_keys("New York")
                    time.sleep(2)

                    keyword_search_button = find_element_by_xpath(browser,KEYWORD_SEARCH_BUTTON)
                    
                    if keyword_search_button:
                       keyword_search_button.click()
                       time.sleep(4)

                    found_jobs = find_element_by_xpath(browser,FOUND_JOBS)
                    ny_found_jobs = extract_integer(found_jobs.text)
                    total_job = TotalJob(site.name,total_found_jobs,ny_found_jobs)
                    total_jobs.append(total_job)
                    print(extract_integer(f"New York:{found_jobs.text}"))
                    

                
                write_objects_to_csv('total_jobs.csv',total_jobs)

            time.sleep(2)

        except Exception:
            print("Something went wrong")
            traceback.print_exc()
        finally:
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


workday_scrape(workday_list)
