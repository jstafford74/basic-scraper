from datetime import datetime


class Company:
    def __init__(self, name, workday_url, website, equity_ticker):
        self.name = name
        self.workday_url = workday_url
        self.website = website
        self.equity_ticker = equity_ticker


class Application:
    def __init__(
        self, employer_name, job_title, job_req_id, status, date_submitted, is_active
    ):
        now = datetime.now()
        dt_string = now.strftime("%m-%d-%Y")
        self.employer_name = employer_name
        self.job_title = job_title
        self.job_req_id = job_req_id
        self.status = status
        self.date_submitted = date_submitted
        self.is_active = is_active
        self.updated_at=dt_string

    def to_dict(self):
        # Convert object properties to a dictionary
        return {
            "employer_name": self.employer_name,
            "job_title": self.job_title,
            "job_req_id": self.job_req_id,
            "status": self.status,
            "date_submitted": self.date_submitted,
            "is_active": self.is_active,
        }
