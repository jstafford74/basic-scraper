import os

from dotenv import load_dotenv
from models import ApplicationStatusModel


class ApplicationStatusController:
    def __init__(self):
        load_dotenv()

        self.model = ApplicationStatusModel(
            os.getenv("DATABASE_NAME"), os.getenv("APPLICATION_STATUS_COLLECTION")
        )

    def create_document(self, data):
        return self.model.create(data)

    def find_one_document(self, filter):
        return self.model.find_one(filter)

    def get_document(self, document_id):
        return self.model.read(document_id)

    def update_document(self, document_id, updates):
        return self.model.update(document_id, updates)
    
    def update_one_document(self, filter, updates,upsert):
        return self.model.update_one(filter, updates,upsert)

    def delete_document(self, document_id):
        return self.model.delete(document_id)

    def get_all_documents(self):
        return self.model.find_all()
    
    def get_all_documents_sorted_by_name(self):
        return self.model.find_all_sorted_by_name()
