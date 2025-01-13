import re

import requests
from bs4 import BeautifulSoup

BASE_TSRY_URL = (
    "https://home.treasury.gov/resource-center/data-chart-center/interest-rates"
)
CURVE_TYPE = "daily_treasury_real_yield_curve"
YEAR_SELECTED = "2025"
MONTH_SELECTED = "01"

CURVES = ["daily_treasury_yield_curve", "daily_treasury_real_yield_curve"]
URL = f"{BASE_TSRY_URL}/TextView?type={CURVE_TYPE}&field_tdr_date_value_month={YEAR_SELECTED}{MONTH_SELECTED}"

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
time_results = soup.find_all("td", class_=re.compile("field-tdr-date"))
compiled_curve = {}
date_regex_pattern = r"^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/\d{4}$"

tenors = {"5_yr": "N/A", "7_yr": "N/A", "10_yr": "N/A", "20_yr": "N/A", "30_yr": "N/A"}
columns = ["5_yr", "7_yr", "10_yr", "20_yr", "30_yr"]

five_yr_header = "field-tc-5year-table-column"
seven_yr_header = "field-tc-7year-table-column"
ten_yr_header = "field-tc-10year-table-column"
twenty_yr_header = "field-tc-20year-table-column"
thirty_yr_header = "field-tc-30year-table-column"

five_year_results = soup.find_all(attrs={"headers": re.compile(five_yr_header)})

seven_year_results = soup.find_all(attrs={"headers": re.compile(seven_yr_header)})

ten_year_results = soup.find_all(attrs={"headers": re.compile(ten_yr_header)})

twenty_year_results = soup.find_all(attrs={"headers": re.compile(twenty_yr_header)})

thirty_year_results = soup.find_all(attrs={"headers": re.compile(thirty_yr_header)})

curves = [
    time_results,
    five_year_results,
    seven_year_results,
    ten_year_results,
    twenty_year_results,
    thirty_year_results,
]


for col_idx, curve in enumerate(curves):
    for date_idx, rate in enumerate(curve):
        if re.search(date_regex_pattern, rate.text.strip()):
            date = rate.time.text.strip()
            compiled_curve[f"{date}"] = tenors
            continue

        cur_rate = float(rate.text.strip())
        date = time_results[date_idx].time.text.strip()
        tenor = columns[col_idx - 1]

        compiled_curve[f"{date}"][f"{tenor}"] = cur_rate


print(compiled_curve)
