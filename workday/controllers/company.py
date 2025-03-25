import os

from dotenv import load_dotenv
from models.company import CompanyModel


class CompanyController:
    def __init__(self):
        load_dotenv()

        self.model = CompanyModel(
            os.getenv("DATABASE_NAME"), os.getenv("COMPANIES_COLLECTION")
        )

    def create_document(self, data):
        return self.model.create(data)

    def get_document(self, document_id):
        return self.model.read(document_id)

    def update_document(self, document_id, updates):
        return self.model.update(document_id, updates)

    def delete_document(self, document_id):
        return self.model.delete(document_id)

    def get_all_documents(self):
        return self.model.find_all()
    
    def get_all_documents_sorted_by_name(self):
        return self.model.find_all_sorted_by_name()
