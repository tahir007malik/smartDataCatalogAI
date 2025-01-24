import openai  # pip install openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key from environment variables for security
openai.api_key = os.getenv("OPENAI_API_KEY")  # You should store your key securely as an environment variable

# Function to generate AI-powered description for columns
def generate_column_description(column_name, column_type):
    prompt = f"Generate a short description for the column '{column_name}' of type '{column_type}' in a database schema."
    
    # Use the correct chat model endpoint
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can also use "gpt-4" if available
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    description = response['choices'][0]['message']['content'].strip()
    return description

# Example of using the function to generate a description
column_name = "age"
column_type = "int"
description = generate_column_description(column_name, column_type)

print(description)