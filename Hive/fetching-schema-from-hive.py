# Description: This script fetches schema from a Hive table and inserts it into MongoDB.
# Run: gcloud compute ssh --zone=<your-cluster-zone> --project=<your-project-id> --ssh-key-file=<path_to_google_compute_engine.pub> -- -L 10000:localhost:10000 <cluster-name>
from pyhive import hive
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Connect to Hive on Dataproc
hive_conn = hive.Connection(host='localhost', port=10000, username='tahir')

# Connect to MongoDB
mongo_client = MongoClient(os.getenv("MONGO_URI"))
db = mongo_client.data_catalog
datasets = db.datasets

# Fetch schema from a table
def fetch_hive_schema(table_name, database='test_db'):
    cursor = hive_conn.cursor()
    cursor.execute(f"DESCRIBE {database}.{table_name}")
    schema = cursor.fetchall()
    columns = [{"name": col[0], "type": col[1], "description": ""} for col in schema if col[0]]
    return columns

# Example: Fetch schema for a table
table_name = "sample_table"
schema = fetch_hive_schema(table_name)

# Insert metadata into MongoDB
metadata = {
    "dataset_name": table_name,
    "description": f"Schema for {table_name}",
    "columns": schema,
    "row_count": None,
    "created_date": "2025-01-11"
}
datasets.insert_one(metadata)
print("Metadata inserted successfully!")