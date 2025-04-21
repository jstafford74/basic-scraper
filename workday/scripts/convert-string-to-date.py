import argparse
import os
from datetime import datetime

from pymongo import MongoClient

## python ./convert_string_to_date.py <collection_name> <date_field>
# Example: python ./convert_string_to_date.py applications measure_date

def convert_string_dates_to_date(collection_name, date_field):
    print(f"Processing collection: {collection_name} with date field: {date_field}")
    # Establish a connection to MongoDB
    MONGO_URI = os.getenv("MONGO_URI")
    client = MongoClient(MONGO_URI)
    
    try:
        db = client["workday"]  # Replace with your database name
        collection = db[collection_name]

        # Find all documents where the date_field is a string
        cursor = collection.find({date_field: {'$type': 'string'}})

        for doc in cursor:
            # Convert the string date into a Date object
            string_date = doc[date_field]  # Using the specified date_field
            
            try:
                 # Adjusting for MM-DD-YYYY format
                date_obj = datetime.strptime(string_date, "%m-%d-%Y")  
            except ValueError:
                print(f"Invalid date format for document ID {doc['_id']}: {string_date}")
                continue
            
            # Update the document with the converted Date object
            collection.update_one(
                {'_id': doc['_id']},  # Filter
                {'$set': {date_field: date_obj}}  # Update operation
            )

        print(f"All string dates in the field '{date_field}' have been converted to Date objects in collection '{collection_name}'.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Convert string dates to Date datatype in MongoDB.")
    parser.add_argument('collection_name', type=str, help='The name of the collection to process')
    parser.add_argument('date_field', type=str, help='The name of the field containing the date strings')

    # Parse the command line arguments
    args = parser.parse_args()
    
    # Call the conversion function with the provided collection name and date field
    convert_string_dates_to_date(args.collection_name, args.date_field)