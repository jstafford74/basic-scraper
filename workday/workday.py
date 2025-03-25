import math
import os
import time
import traceback
from datetime import datetime

from application import Application
from bson import ObjectId
from constants import (
    CLEAR_ALL,
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
    STATE_SEARCHES,
    STATUS_TABS_SECTION,
    UTILITY_BUTTON,
)
from controllers import CompanyController
from dotenv import load_dotenv
from pymongo import MongoClient
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
    instantiate_browser,
)


class WorkdaySite:
    def __init__(self, name, url, email, password):
        self.name = name
        self.url = url
        self.email = email
        self.password = password


workday_list = [WorkdaySite(**data) for data in workday_data]


def workday_scrape(run_search=True, run_apps=True):
    # Load environment variables
    load_dotenv()

    MONGO_URI = os.getenv("MONGO_URI")

    client = MongoClient(MONGO_URI)
    print("✅ Connected Databases:", client.list_database_names())

    db = client.workday

    company_controller = CompanyController()
    # companies_collection = db.companies
    applications_collection = db.applications
    snapshots_collection = db.opening_snapshots
    application_status_collection = db.application_statuses

    sites_list = company_controller.get_all_documents_sorted_by_name()
    print(sites_list)
    # Start the timer
    start_time = time.time()
    now = datetime.now()
    dt_string = now.strftime("%m-%d-%Y")

    for site in sites_list:
        company_id = ObjectId(site["_id"])

        browser = instantiate_browser()

        print(f"Visiting {site['name']} at {site['url']}")
        browser.get(site["url"])
        # pause for username & password entry
        time.sleep(2)

        # ===============LOGIN===============
        try:
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

            # Find Active & Inactive Tabs

            status_tabs = find_elements_by_xpath(browser, STATUS_TABS_SECTION)

            active_button_text = (
                status_tabs[0].text if status_tabs and len(status_tabs) else None
            )
            inactive_button_text = (
                status_tabs[1].text if status_tabs and len(status_tabs) else None
            )
            # print(f"active tabs:{active_button_text}")
            # print(f"iactive tabs:{inactive_button_text}")
            active_apps = (
                extract_integer(active_button_text) if active_button_text else 0
            )
            inactive_apps = (
                extract_integer(inactive_button_text) if inactive_button_text else 0
            )
            print(f"active tabs:{active_apps}")
            print(f"iactive tabs:{inactive_apps}")

            active_app_upper_limit = (
                math.ceil(int(active_apps) / 4) if active_apps else 0
            )
            inactive_app_upper_limit = (
                math.ceil(int(inactive_apps) / 4) if inactive_apps else 0
            )
            current_app_status = application_status_collection.find_one(
                {"measure_date": dt_string}
            )

            is_upsert = True if current_app_status is None else False

            if active_apps > 0:
                active_apps_update = application_status_collection.update_one(
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
                inactive_apps_update = application_status_collection.update_one(
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
            
            # //START active tab iteration
            if run_apps:
                active_job_reqs = []
                inactive_job_reqs = []
                for i in range(1, active_app_upper_limit + 1):
                    print(f"iteration: {i}")
                    # time.sleep(2)
                    job_title_column = find_elements_by_xpath(
                        browser, f"//{PARENT_TABPANEL_DIV}//{JOB_TITLE_COLUMN}"
                    )
                    job_req_column = find_elements_by_xpath(
                        browser, f"//{PARENT_TABPANEL_DIV}//{JOB_REQ_COLUMN}"
                    )
                    status_column = find_elements_by_xpath(
                        browser, f"//{PARENT_TABPANEL_DIV}//{JOB_STATUS_COLUMN}"
                    )
                    date_submitted_column = find_elements_by_xpath(
                        browser, f"//{PARENT_TABPANEL_DIV}//{DATE_SUBMITTED_COLUMN}"
                    )
                    for idx, row in enumerate(job_title_column):
                        job_title = row.text
                        job_req_id = job_req_column[idx].text
                        job_status = status_column[idx].text
                        date_submitted = date_submitted_column[idx].text

                        job_app = Application(
                            company_id,
                            job_title,
                            job_req_id,
                            job_status,
                            date_submitted,
                            is_active=True,
                        )

                        # Insert application
                        application_to_find = {
                            "company_id": company_id,
                            "job_req_id": job_req_id,
                            "status": job_status,
                        }

                        active_result = applications_collection.find_one(
                            application_to_find
                        )

                        active_job_reqs.append(job_req_id)

                        if active_result is None:
                            new_app = applications_collection.insert_one(
                                job_app.to_dict()
                            )
                            if new_app.acknowledged:
                                print(f"{site['name']} new app inserted")
                            else:
                                print(
                                    "something went wrong with new active app insertion"
                                )

                        else:
                            if job_status == active_result["status"]:
                                print("job status' match, no update needed")

                            else:
                                active_app_update = applications_collection.update_one(
                                    {
                                        "company_id": company_id,
                                        "job_req_id": job_req_id,
                                    },
                                    {"$set": {"status": job_status}},
                                )
                                if active_app_update.acknowledged:
                                    print(f"{site['name']} new app inserted")
                                else:
                                    print(
                                        "something went wrong with new active app insertion"
                                    )
                    time.sleep(1)

                    has_pagination = find_elements_by_xpath(
                        browser, f"//{PARENT_TABPANEL_DIV}//{PAGINATION_NAV}"
                    )
                    if not has_pagination:
                        print("no pagination present")
                    else:
                        next_button = find_element_by_xpath(
                            browser,
                            f"//{PARENT_TABPANEL_DIV}//{PAGINATION_NAV}//{NEXT_BUTTON}",
                        )
                        print("Clicking Next Button")
                        next_button.click()
                        time.sleep(1)

                    if len(active_job_reqs) and idx == len(job_title_column) - 1:
                        active_job_update = company_controller.update_document(
                            company_id,
                            {"active_applications": active_job_reqs},
                        )
                        if active_job_update:
                            print(f"{site['name']} active apps updated successfully.")
                        else:
                            print("No document found or document was not modified.")

                # //END active tab iteration

                # //START inactive tab iteration
                if status_tabs and len(status_tabs):
                    status_tabs[1].click()

                if int(inactive_apps) > 0:
                    for i in range(1, inactive_app_upper_limit + 1):
                        print(f"inactive iteration: {i}")
                        # time.sleep(2)
                        inactive_job_title_column = find_elements_by_xpath(
                            browser, f"//{PARENT_TABPANEL_DIV}//{JOB_TITLE_COLUMN}"
                        )
                        inactive_job_req_column = find_elements_by_xpath(
                            browser, f"//{PARENT_TABPANEL_DIV}//{JOB_REQ_COLUMN}"
                        )
                        inactive_status_column = find_elements_by_xpath(
                            browser, f"//{PARENT_TABPANEL_DIV}//{JOB_STATUS_COLUMN}"
                        )
                        inactive_date_submitted_column = find_elements_by_xpath(
                            browser, f"//{PARENT_TABPANEL_DIV}//{DATE_SUBMITTED_COLUMN}"
                        )
                        for idx, row in enumerate(inactive_job_title_column):
                            job_title = row.text
                            job_req_id = inactive_job_req_column[idx].text
                            job_status = inactive_status_column[idx].text
                            date_submitted = inactive_date_submitted_column[idx].text

                            job_app = Application(
                                company_id,
                                job_title,
                                job_req_id,
                                job_status,
                                date_submitted,
                                is_active=False,
                            )
                            # Insert application
                            application_to_find = {
                                "company_id": company_id,
                                "job_req_id": job_req_id,
                                "status": job_status,
                            }

                            inactive_result = applications_collection.find_one(
                                application_to_find
                            )

                            inactive_job_reqs.append(job_req_id)

                            if inactive_result is None:
                                print("result is None")
                                applications_collection.insert_one(job_app.to_dict())
                            else:
                                print("result is not None")
                                if job_status == inactive_result["status"]:
                                    print("job status' match")
                                else:
                                    applications_collection.update_one(
                                        {
                                            "company_id": company_id,
                                            "job_req_id": job_req_id,
                                        },
                                        {"$set": {"status": job_status}},
                                    )

                        time.sleep(2)
                        print("=====Checking for inactive Pagination=====")
                        has_pagination = find_elements_by_xpath(
                            browser, f"//{PARENT_TABPANEL_DIV}//{PAGINATION_NAV}"
                        )
                        if not has_pagination:
                            print("no pagination present")
                        else:
                            next_button = (
                                find_element_by_xpath(
                                    browser,
                                    f"//{PARENT_TABPANEL_DIV}//{PAGINATION_NAV}//{NEXT_BUTTON}",
                                )
                                if len(has_pagination)
                                else False
                            )
                            print("Clicking Next Button")
                            next_button.click()
                            time.sleep(2)

                        if (
                            len(inactive_job_reqs)
                            and idx == len(inactive_job_title_column) - 1
                        ):
                            company_controller.update_document(
                                company_id,
                                {"inactive_applications": inactive_job_reqs},
                            )

                # //END active tab iteration

            if run_search:
                search_jobs = find_element_by_xpath(browser, SEARCH_FOR_JOBS)

                if search_jobs:
                    print("clicking on search for jobs")
                    search_jobs.click()
                    time.sleep(3)

                    found_jobs_element = find_element_by_xpath(browser, FOUND_JOBS)
                    total_found_jobs = (
                        extract_integer(found_jobs_element.text)
                        if found_jobs_element
                        else 0
                    )

                    total_snapshot_update = snapshots_collection.update_one(
                        {
                            "company_id": company_id,
                            "snapshot_date": dt_string,
                        },
                        {
                            "$set": {
                                "total": total_found_jobs,
                            },
                        },
                        upsert=True,
                    )

                    if total_snapshot_update.modified_count > 0:
                        print(f"{site['name']} Document updated successfully.")
                    else:
                        print("No document found or document was not modified.")

                    keyword_search = find_element_by_xpath(
                        browser, KEYWORD_SEARCH_INPUT
                    )

                    if keyword_search:
                        keyword_search_button = find_element_by_xpath(
                            browser, KEYWORD_SEARCH_BUTTON
                        )

                        for state in STATE_SEARCHES:
                            for key, value in state.items():
                                keyword_search.click()
                                keyword_search.clear()
                                keyword_search.send_keys(value)
                                time.sleep(2)

                                if keyword_search_button:
                                    keyword_search_button.click()
                                    time.sleep(4)

                                found_jobs_element = find_element_by_xpath(
                                    browser, FOUND_JOBS
                                )

                                current_found_jobs = extract_integer(
                                    found_jobs_element.text
                                )

                                current_search_snapshot = (
                                    snapshots_collection.find_one_and_update(
                                        {
                                            "company_id": company_id,
                                            "snapshot_date": dt_string,
                                        },
                                        {
                                            "$set": {key: current_found_jobs},
                                        },
                                    )
                                )

                                if current_search_snapshot["_id"]:
                                    print(f"{site['name']} {key} snapshot updated:")
                                else:
                                    print(
                                        "No document found or document was not modified."
                                    )

                            clear_all_button = find_element_by_xpath(browser, CLEAR_ALL)
                            if clear_all_button:
                                clear_all_button.click()
                                time.sleep(2)

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

    # End the timer
    end_time = time.time()

    # Calculate elapsed time
    elapsed_time = end_time - start_time
    minutes, seconds = divmod(elapsed_time, 60)

    # Display the result
    print(
        f"Workday scrape of {len(sites_list)} sites completed in {int(minutes)} minutes and {seconds:.2f} seconds."
    )


workday_scrape(run_search=False, run_apps=False)
