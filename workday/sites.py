import os

from dotenv import load_dotenv

load_dotenv()

workday_data = [
    {
        "name": "Capital One",
        "url": os.getenv("CAPITAL_ONE_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "Mitsubishi Bank",
        "url": os.getenv("MUFG_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "TD Bank",
        "url": os.getenv("TD_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "Bank of America",
        "url": os.getenv("BANK_AMERICA_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "Wells Fargo",
        "url": os.getenv("WELLS_FARGO_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "Synchrony",
        "url": os.getenv("SYNCHRONY_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "Freddie Mac",
        "url": os.getenv("FREDDIE_MAC_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "T Rowe",
        "url": os.getenv("TROWE_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "PWC",
        "url": os.getenv("PWC_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "Mastercard",
        "url": os.getenv("MASTERCARD_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "G Research",
        "url": os.getenv("G_RESEARCH_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "Wellington",
        "url": os.getenv("WELLINGTON_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "Russel Investments",
        "url": os.getenv("RUSSELL_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "Mizuho",
        "url": os.getenv("MIZUHO_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "Gartner",
        "url": os.getenv("GARTNER_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "Northern Trust",
        "url": os.getenv("NORTHERN_TRUST_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "Santander",
        "url": os.getenv("SANTANDER_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "PNC Bank",
        "url": os.getenv("PNC_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "US Bank",
        "url": os.getenv("US_BANK_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "Citibank",
        "url": os.getenv("CITIBANK_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "Pitney Bowes",
        "url": os.getenv("PITNEY_BOWES_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "Deutsche Bank",
        "url": os.getenv("DB_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "RBS",
        "url": os.getenv("RBS_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "Apple Bank",
        "url": os.getenv("APPLE_BANK_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "Franklin Investments",
        "url": os.getenv("FRANKLIN_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "Barclays",
        "url": os.getenv("BARCLAYS_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    },
    {
        "name": "General Motors",
        "url": os.getenv("GENERAL_MOTORS_URL"),
        "email": os.getenv("DEFAULT_EMAIL"),
        "password": os.getenv("DEFAULT_PASSWORD"),
    }
]

