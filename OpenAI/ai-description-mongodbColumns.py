from pymongo import MongoClient
from dotenv import load_dotenv
import openai
import os

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key from environment variables for security
openai.api_key = os.getenv("OPENAI_API_KEY")

# MongoDB connection details
MONGO_URI = os.getenv("MONGO_URI")  # MongoDB connection URI
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Function to generate AI-powered description for columns
def generate_column_description(column_name, column_type):
    # Formulate the chat-based prompt
    messages = [
        {
            "role": "system",
            "content": "You are an assistant specialized in generating concise database column descriptions.",
        },
        {
            "role": "user",
            "content": f"Generate a short description for the column '{column_name}' of type '{column_type}' in a database schema.",
        },
    ]
    
    # Call the chat endpoint
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can also use "gpt-4" if available
        messages=messages,
        max_tokens=100,
        temperature=0.7
    )
    
    description = response["choices"][0]["message"]["content"].strip()
    return description


# Connect to MongoDB and get column names and types
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Get a sample document to determine field names and types
sample_document = collection.find_one()  # You can also use .find() to get multiple documents
if sample_document is None:
    print("No documents found in the collection.")
else:
    columns = []
    for column_name, column_value in sample_document.items():
        column_type = type(column_value).__name__
        columns.append((column_name, column_type))

    # Proceed with generating descriptions if columns are found
    descriptions = {}
    for column_name, column_type in columns:
        description = generate_column_description(column_name, column_type)
        descriptions[column_name] = description

    # Store the descriptions in MongoDB (add a new field or a new collection)
    collection.update_one(
        {
                "_id": sample_document["_id"]
            },  # You can loop over all documents if needed
        {
                "$set": {
                    "column_descriptions": descriptions
                    }
            }
    )

    # Print out the generated descriptions
    print(descriptions)