import pandas as pd
from datetime import datetime
import src.database as db


def clean_date(date_str):
    """Convert date string to ISO format (YYYY-MM-DD)."""
    try:
        dt = pd.to_datetime(date_str)
        return dt.strftime("%Y-%m-%d")
    except Exception as e:
        print(f"Date parsing error: {e} for date {date_str}")
        return None


def load_csv(file_path):
    """Load CSV file into Pandas DataFrame and clean data."""
    df = pd.read_csv(file_path)
    
    # Example expected columns: Date, Amount, Type, Category, Description, Tags
    # Adjust based on actual CSV format
    
    # Clean and rename columns to expected names
    df.rename(columns=lambda x: x.strip().lower(), inplace=True)
    
    # Ensure required columns exist
    required_cols = ['date', 'amount', 'type']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Clean date column
    df['date'] = df['date'].apply(clean_date)
    df.dropna(subset=['date'], inplace=True)

    # Clean amount column
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df.dropna(subset=['amount'], inplace=True)

    # Clean type column and normalize
    df['type'] = df['type'].str.lower().str.strip()
    valid_types = ['income', 'expense', 'investment']
    df = df[df['type'].isin(valid_types)]

    # Fill optional columns if missing
    if 'category' not in df.columns:
        df['category'] = None
    if 'description' not in df.columns:
        df['description'] = None
    if 'tags' not in df.columns:
        df['tags'] = None

    return df


def get_or_create_category(category_name):
    """Get category id from DB or create new category if not exists."""
    # Simplified example - extend as needed for hierarchy
    categories = db.execute_query("SELECT category_id, name FROM categories")
    cat_dict = {name.lower(): cid for cid, name in categories} if categories else {}

    cat_name_lower = category_name.lower() if category_name else None
    if cat_name_lower in cat_dict:
        return cat_dict[cat_name_lower]

    # Create new category (if name provided)
    if category_name:
        db.execute_query("INSERT INTO categories (name) VALUES (?)", (category_name,))
        # Get the new category id
        categories = db.execute_query("SELECT category_id, name FROM categories")
        cat_dict = {name.lower(): cid for cid, name in categories}
        return cat_dict.get(cat_name_lower)
    
    return None


def ingest_transactions_from_df(df, user_id=None):
    """Load cleaned DataFrame transactions into the database."""
    for _, row in df.iterrows():
        category_id = get_or_create_category(row['category']) if row['category'] else None
        db.add_transaction(
            date=row['date'],
            amount=row['amount'],
            txn_type=row['type'],
            category_id=category_id,
            description=row.get('description'),
            tags=row.get('tags'),
            user_id=user_id
        )


def ingest_csv(file_path, user_id=None):
    """Complete ingestion pipeline: load, clean, import CSV."""
    print(f"Loading CSV data from: {file_path}")
    df = load_csv(file_path)
    print(f"Loaded {len(df)} records, ingesting into database...")
    ingest_transactions_from_df(df, user_id)
    print("Data ingestion complete.")


if __name__ == "__main__":
    # Example usage:
    test_csv = "data/raw/sample_bank_statement.csv"
    ingest_csv(test_csv)
