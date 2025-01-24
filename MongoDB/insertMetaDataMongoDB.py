# Description: This script inserts metadata about a dataset into a MongoDB collection.
# Create a database `data_catalog` and a collection `datasets` in MongoDB Atlas
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client.data_catalog
datasets = db.datasets

# Example metadata
metadata = {
    "dataset_name": "Customer Data",
    "description": "Contains customer demographics and purchasing habits.",
    "columns": [
        {"name": "CustomerID", "type": "String", "description": "Unique identifier for each customer"},
        {"name": "Age", "type": "Integer", "description": "Age of the customer"},
        {"name": "PurchaseAmount", "type": "Float", "description": "Total amount spent by the customer"}
    ],
    "row_count": 100000,
    "created_date": "2025-01-11"
}

# Insert into MongoDB
datasets.insert_one(metadata)
print("Metadata inserted successfully!")