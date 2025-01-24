from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json
from bson import ObjectId

load_dotenv()

# Fetch environment variables
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Custom serializer for ObjectId
def serialize_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError("Type not serializable")

result = collection.find()
if result is not None:
    for i in result:
        # Pretty-print the result
        print(json.dumps(i, indent=4, default=serialize_objectid))
        print("\n" + "=" * 80 + "\n") 
else:
    print("No documents found in the collection.")