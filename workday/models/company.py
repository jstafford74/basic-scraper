import os

from bson import ObjectId
from dotenv import load_dotenv
from pymongo import ASCENDING, MongoClient


class CompanyModel:
    def __init__(self, database_name, collection_name):
        load_dotenv()
        MONGO_URI = os.getenv("MONGO_URI")
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def create(self, document):
        return self.collection.insert_one(document)

    def read(self, document_id):
        return self.collection.find_one({"_id": ObjectId(document_id)})

    def update(self, document_id, updates):
        return self.collection.update_one(
            {"_id": ObjectId(document_id)}, {"$set": updates}
        )

    def delete(self, document_id):
        return self.collection.delete_one({"_id": ObjectId(document_id)})

    def find_all(self):
        return list(self.collection.find())

    def find_all_sorted_by_name(self):
        documents = list(self.collection.find().sort("name", ASCENDING))
        return documents
