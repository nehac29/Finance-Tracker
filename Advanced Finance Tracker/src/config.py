import os

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
EXPORT_DATA_DIR = os.path.join(DATA_DIR, "export")

DB_DIR = os.path.join(BASE_DIR, "db")
DB_PATH = os.path.join(DB_DIR, "finance.db")

# File paths
SCHEMA_PATH = os.path.join(DB_DIR, "schema.sql")

# Other configurations
DATE_FORMAT = "%Y-%m-%d"

# Ensure folders exist (optional)
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, EXPORT_DATA_DIR, DB_DIR]:
    os.makedirs(directory, exist_ok=True)
