import os
import pandas as pd
from datetime import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# MONGO DB CONNECTION
MONGOPW = os.getenv("MONGOPW")
uri = f"mongodb+srv://tima:{MONGOPW}@bnuy-1.3kon4.mongodb.net/?retryWrites=true&w=majority&appName=bnuy-1"
client = MongoClient(uri, server_api=ServerApi('1'))
mongo_db = client["t-site"]

# Load DataFrame from CSV
bins = pd.read_csv('pasturize/pasturized-jugs-nochill.csv').to_dict("records")
flow = pd.read_csv('pasturize/pasturized-milk-nochill.csv').to_dict("records")

def rewrite_daily_collection(data, collection_name):
    """Updates MongoDB collection by upserting new data."""
    mongo_collection = mongo_db[collection_name]
    # Drop the collection (delete all documents)
    mongo_collection.drop()
    # Insert new data
    mongo_collection.insert_many(data)
    print(f"collection:{collection_name} updated at {datetime.now()}.")

rewrite_daily_collection(bins, 'nochill-dist')
rewrite_daily_collection(flow, 'nochill-flow')

def update_database(data, collection_name, id_tag):
    """Updates MongoDB collection by upserting new data."""
    mongo_collection = mongo_db[collection_name]
    mongo_collection.drop()

    mongo_collection.insert_many(data)

    for record in data:
        filter_query = {id_tag: record[id_tag]}  # Match by unique ID
        update_query = {"$set": record}  # Update fields if exists
        mongo_collection.update_one(filter_query, update_query, upsert=True)
    
    print(f"collection:{collection_name} updated at {datetime.now()}.")

client.close()


