import math
import time
import traceback
from datetime import datetime, timezone

from bson import ObjectId
from classes.application import Application
from constants import (
    CLEAR_ALL,
    DATE_SUBMITTED_COLUMN,
    JOB_REQ_COLUMN,
    JOB_STATUS_COLUMN,
    JOB_TITLE_COLUMN,
    NEXT_BUTTON,
    ORGANIC_SEARCHES,
    PAGINATION_NAV,
    PARENT_TABPANEL_DIV,
    STATE_SEARCHES,
)
from controllers import ApplicationsController, CompanyController, SnapshotsController
from dotenv import load_dotenv
from search import (
    BARCLAYS_SEARCH_FOR_JOBS,
    FOUND_JOBS,
    KEYWORD_SEARCH_BUTTON,
    KEYWORD_SEARCH_INPUT,
    SEARCH_FOR_JOBS,
)
from utils import (
    extract_integer,
    find_active_and_inactive_tabs,
    find_element_by_xpath,
    find_elements_by_xpath,
    instantiate_browser,
    login,
    logout,
)


def workday_scrape(run_search=True, run_apps=True):
    # Load environment variables
    load_dotenv()

    applications_controller = ApplicationsController()
    company_controller = CompanyController()
    snapshots_controller = SnapshotsController()

    sites_list = company_controller.get_all_documents_sorted_by_name()
    print(f"sites in db: {len(sites_list)}")
    # Start the timer
    start_time = time.time()

    current_date = datetime.now(timezone.utc)

    for site in sites_list:
        company_id = ObjectId(site["_id"])

        browser = instantiate_browser()

        print(f"Visiting {site['name']} at {site['url']}")

        base_url = site["url"].replace("/login", "")
        browser.get(base_url)

        time.sleep(2)

        # ===============LOGIN===============
        try:
            if run_search:
                # print(site)
                # Get the current date at midnight
                # today = datetime.now().replace(
                #     hour=0, minute=0, second=0, microsecond=0
                # )

                # # Create the end of today (optional if necessary for the query)
                # end_of_today = today + timedelta(days=1)  # Start of tomorrow

                # print(f"today: {today}")
                # print(f"end of today: {end_of_today}")
                # # Query to find a snapshot with the current date
                # snapshot = snapshots_controller.find_one_document(
                #     {"snapshot_date": {"$gte": today, "$lt": end_of_today}}
                # )
                # print(f"snapshot: {snapshot}")
                # if snapshot is None:
                    if site["name"] == "Barclays":
                        search_jobs = find_element_by_xpath(
                            browser, BARCLAYS_SEARCH_FOR_JOBS
                        )
                    if site["name"] in ORGANIC_SEARCHES:
                        search_jobs = None
                    else:
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

                    total_snapshot_update = snapshots_controller.create_document(
                        {
                            "total": total_found_jobs,
                            "company_id": company_id,
                            "snapshot_date": current_date,
                        },
                    )
                    if total_snapshot_update.acknowledged:
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
                                    snapshots_controller.update_one_document(
                                        {
                                            "_id": total_snapshot_update.inserted_id,
                                        },
                                        {
                                            "$set": {key: current_found_jobs},
                                        },
                                        upsert=True,
                                    )
                                )
                                if current_search_snapshot.acknowledged:
                                    print(f"{site['name']} {key} snapshot updated:")
                                else:
                                    print(
                                        "No document found or document was not modified."
                                    )
                            clear_all_button = find_element_by_xpath(browser, CLEAR_ALL)
                            if clear_all_button:
                                clear_all_button.click()
                                time.sleep(2)
                # else:
                #     print(f"Snapshot already created for today: {site['name']}")
            if site["password"]:
                # Find the log in elements
                browser.get(site["url"])
                time.sleep(2)
                login(browser, site)

                active_apps, inactive_apps, status_tabs = find_active_and_inactive_tabs(
                    browser, site
                )

                active_app_upper_limit = (
                    math.ceil(int(active_apps) / 4) if active_apps else 0
                )
                inactive_app_upper_limit = (
                    math.ceil(int(inactive_apps) / 4) if inactive_apps else 0
                )
                print(f"Site: {site['name']}")
                print(f"Active Tabs: {active_apps}")
                print(f"Inactive Tabs: {inactive_apps}")

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

                            active_result = applications_controller.find_one_document(
                                application_to_find
                            )

                            active_job_reqs.append(job_req_id)

                            if active_result is None:
                                new_app = applications_controller.create_document(
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
                                    active_app_update = (
                                        applications_controller.update_one_document(
                                            {
                                                "company_id": company_id,
                                                "job_req_id": job_req_id,
                                            },
                                            {"$set": {"status": job_status}},
                                        )
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
                                print(
                                    f"{site['name']} active apps updated successfully."
                                )
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
                                browser,
                                f"//{PARENT_TABPANEL_DIV}//{DATE_SUBMITTED_COLUMN}",
                            )
                            for idx, row in enumerate(inactive_job_title_column):
                                job_title = row.text
                                job_req_id = inactive_job_req_column[idx].text
                                job_status = inactive_status_column[idx].text
                                date_submitted = inactive_date_submitted_column[
                                    idx
                                ].text

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

                                inactive_result = (
                                    applications_controller.find_one_document(
                                        application_to_find
                                    )
                                )

                                inactive_job_reqs.append(job_req_id)

                                if inactive_result is None:
                                    print("result is None")
                                    applications_controller.create_document(
                                        job_app.to_dict()
                                    )
                                else:
                                    print("result is not None")
                                    if job_status == inactive_result["status"]:
                                        print("job status' match")
                                    else:
                                        applications_controller.update_one_document(
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

                    time.sleep(2)

        except Exception:
            print("Something went wrong")
            traceback.print_exc()
        finally:
            logout(browser)

    # End the timer
    end_time = time.time()

    # Calculate elapsed time
    elapsed_time = end_time - start_time
    minutes, seconds = divmod(elapsed_time, 60)

    # Display the result
    print(
        f"Workday scrape of {len(sites_list)} sites completed in {int(minutes)} minutes and {seconds:.2f} seconds."
    )


workday_scrape(run_search=True, run_apps=True)
