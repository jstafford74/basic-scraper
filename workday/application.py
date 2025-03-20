from datetime import datetime


class Company:
    def __init__(self, name, workday_url, website, equity_ticker):
        self.name = name
        self.workday_url = workday_url
        self.website = website
        self.equity_ticker = equity_ticker


class Application:
    def __init__(
        self, company_id, job_title, job_req_id, status, date_submitted, is_active
    ):
        now = datetime.now()
        dt_string = now.strftime("%m-%d-%Y")
        self.company_id = company_id
        self.job_title = job_title
        self.job_req_id = job_req_id
        self.status = status
        self.date_submitted = date_submitted
        self.is_active = is_active
        self.updated_at = dt_string

    def to_dict(self):
        # Convert object properties to a dictionary
        return {
            "company_id": self.company_id,
            "job_title": self.job_title,
            "job_req_id": self.job_req_id,
            "status": self.status,
            "date_submitted": self.date_submitted,
            "is_active": self.is_active,
            "updated_at": self.updated_at,
        }


class TotalJob:
    def __init__(
        self,
        employer_name,
        total_jobs,
        usa=0,
        new_york=0,
        connecticut=0,
        texas=0,
        massachusetts=0,
        new_jersey=0,
        maryland=0,
        north_carolina=0,
        florida=0,
        california=0,
    ):
        now = datetime.now()
        dt_string = now.strftime("%m-%d-%Y")
        self.employer_name = employer_name
        self.total_jobs = total_jobs
        self.usa = usa
        self.new_york = new_york
        self.connecticut = connecticut
        self.texas = texas
        self.massachusetts = massachusetts
        self.new_jersey = new_jersey
        self.maryland = maryland
        self.north_carolina = north_carolina
        self.florida = florida
        self.california = california
        self.updated_at = dt_string

    def __repr__(self):
        return str(self.__dict__)

    def to_dict(self):
        # Convert object properties to a dictionary
        return {
            "employer_name": self.employer_name,
            "total_jobs": self.total_jobs,
            "usa": self.usa,
            "ny_jobs": self.new_york,
            "connecticut": self.connecticut,
            "texas": self.texas,
            "massachusetts": self.massachusetts,
            "new_jersey": self.new_jersey,
            "maryland": self.maryland,
            "north_carolina": self.north_carolina,
            "florida": self.florida,
            "california": self.california,
            "updated_at": self.updated_at,
        }
    
  
