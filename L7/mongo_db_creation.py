from pymongo import MongoClient
import json

DATA_FILE = "mongo_data.json"
MONGO_CLIENT = "mongodb://localhost:27017/"
DB_NAME = "formula1"

def create_mongo_db():
    # Connect to local MongoDB (default host and port)
    client = MongoClient(MONGO_CLIENT)

    # Create (or connect to) database
    db = client[DB_NAME]

    # Load JSON file
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Loop through each "collection"
    for collection_name, documents in data.items():
        collection = db[collection_name]
        if isinstance(documents, list):
            collection.insert_many(documents)
        else:
            collection.insert_one(documents)

    print("All collections imported successfully.")