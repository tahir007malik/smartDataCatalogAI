import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key from environment variables for security
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate AI-powered description for columns
def generate_column_description(column_name, column_type):
    prompt = f"Generate a short description for the column '{column_name}' of type '{column_type}' in a database schema."
    
    response = openai.ChatCompletion.create(  # Use ChatCompletion.create instead
        model="gpt-3.5-turbo",  # You can also use "gpt-4" if available
        messages=[{"role": "user", "content": prompt}],  # Send the prompt as a message
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )
    
    description = response['choices'][0]['message']['content'].strip()
    return description

# Function to generate descriptions for multiple columns
def generate_multiple_column_descriptions(columns):
    descriptions = {}
    for column_name, column_type in columns:
        descriptions[column_name] = generate_column_description(column_name, column_type)
    return descriptions

# Example usage
columns = [
    ("age", "int"),
    ("name", "varchar"),
    ("created_at", "timestamp"),
    ("price", "decimal")
]

# Generate descriptions for all columns
descriptions = generate_multiple_column_descriptions(columns)

# Print the descriptions
for column_name, description in descriptions.items():
    print(f"Column: {column_name}\nDescription: {description}\n")
