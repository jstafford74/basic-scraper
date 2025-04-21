PARENT_TABPANEL_DIV = "div[@role='tabpanel' and not(@hidden)]"
PAGINATION_NAV = "nav[@data-automation-id='pagination']"
NEXT_BUTTON = "button[@aria-label='Next' and not(@aria-disabled='True')]"
JOB_TITLE_COLUMN = "div[@data-automation-id='applicationTitle']"
JOB_REQ_COLUMN = "td[@class='css-x4yhc3']"
JOB_STATUS_COLUMN = "div[@data-automation-id='applicationStatus']"
DATE_SUBMITTED_COLUMN = "td[@class='css-62prxo']"
ACCOUNT_SETTINGS_ID = "accountSettingsButton"
EMAIL_FIELD_ID = "input-4"
PASSWORD_FIELD_ID = "input-5"
SIGN_IN_CLASS = "css-1s1r74k"
SIGN_OUT_BUTTON = "//button[@aria-label='Sign Out']"
STATUS_TABS_SECTION = (
    "//section[@data-automation-id='applicationsSectionHeading']//button[@role='tab']"
)
UTILITY_BUTTON = "//button[@id='accountSettingsButton']"
STATE_SEARCHES = [
    {"new_york": "New York"},
    {"connecticut": "Connecticut"},
    {"texas": "Texas"},
    {"massachusetts": "Massachusetts"},
    {"new_jersey": "New Jersey"},
    {"maryland": "Maryland"},
    {"north_carolina": "North Carolina"},
    {"florida": "Florida"},
    {"california": "California"},
    {"remote": "Remote"},
    {"intern": "Intern"},
    {"director": "Director"},
    {"analyst": "Analyst"},
    {"manager": "Manager"},
    {"software": "Software"},
    {"engineer": "Engineer"},
    {"project": "Project"},
]

CLEAR_ALL = "//button[@data-automation-id='clearAllButton']"
'<div role="tablist" aria-labelledby="myApplicationsTitle"><button role="tab" '


DISTANCE_LOCATION_BUTTON = "data-automation-id='distanceLocation'"

ORGANIC_SEARCHES=[
    "Adobe Inc.",
    "Coca Cola Company",
    "Millenium",
    "Qualcomm",
    "Truist",
]
