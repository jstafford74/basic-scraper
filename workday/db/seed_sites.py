import os
from datetime import datetime

# import finnhub
# import yfinance as yf
from dotenv import load_dotenv
from pymongo import MongoClient

from workday.db.sites import workday_data

# Initialize the client
# finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
print("✅ Connected Databases:", client.list_database_names())

db = client.workday

companies_collection = db.companies
print(f"Connected to the {companies_collection} in mongoDB")

now = datetime.now()
dt_string = now.strftime("%m-%d-%Y")

updated_workday_data = [
    {**company, "updated_at": dt_string}
    for company in workday_data
]

result = companies_collection.insert_many(updated_workday_data)

print(result.inserted_ids)

client.close()