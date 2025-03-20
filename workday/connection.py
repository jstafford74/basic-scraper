import os

from dotenv import load_dotenv
from pymongo import MongoClient

# Initialize the client
# finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
print("✅ Connected Databases:", client.list_database_names())

db = client.workday

companies_collection = db.companies

cursor = companies_collection.find()

for company in cursor:
    print(company['_id'])