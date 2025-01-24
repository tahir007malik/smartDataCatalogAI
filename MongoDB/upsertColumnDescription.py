import openai
import pymongo
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# OpenAI API setup
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate AI-powered description for a column
def generate_column_description(column_name, column_type):
    system_prompt = (
        "You are a database documentation assistant. Generate short, concise, and context-appropriate descriptions for database fields."
    )
    user_prompt = f"Generate a description for the column '{column_name}' of type '{column_type}' in a database schema."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=100,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# Process and update all documents
for document in collection.find():
    field_descriptions = {}
    for field, value in document.items():
        column_type = type(value).__name__  # Get Python type as a proxy for database type
        description = generate_column_description(field, column_type)
        field_descriptions[field] = description

    # Update the document in MongoDB
    collection.update_one(
        {"_id": document["_id"]},
        {"$set": {"field_descriptions": field_descriptions}}
    )
    print(f"Updated document with _id: {document['_id']}")

print("All documents updated with AI-generated field descriptions.")
