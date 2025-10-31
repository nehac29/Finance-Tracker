import sqlite3
from sqlite3 import Error
from contextlib import closing

DB_PATH = "db/finance.db"  # Database file path


def create_connection(db_path=DB_PATH):
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        print(f"Connected to SQLite database at {db_path}")
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn


def initialize_db():
    """Create tables based on schema.sql file."""
    try:
        with open("db/schema.sql", "r") as f:
            schema_sql = f.read()
        conn = create_connection()
        with closing(conn.cursor()) as cursor:
            cursor.executescript(schema_sql)
        conn.commit()
        print("Database schema initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize database schema: {e}")
    finally:
        if conn:
            conn.close()


def execute_query(query, params=None):
    """Execute a single query with optional parameters."""
    conn = create_connection()
    res = None
    try:
        with closing(conn.cursor()) as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            res = cursor.fetchall()
        conn.commit()
        return res
    except Error as e:
        print(f"Database query failed: {e}")
        return None
    finally:
        if conn:
            conn.close()


# CRUD functions for transactions table

def add_transaction(date, amount, txn_type, category_id=None, description=None, tags=None, user_id=None):
    query = """
    INSERT INTO transactions (date, amount, type, category_id, description, tags, user_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    params = (date, amount, txn_type, category_id, description, tags, user_id)
    execute_query(query, params)
    print("Transaction added.")


def get_transactions(user_id=None):
    if user_id:
        query = "SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC"
        return execute_query(query, (user_id,))
    else:
        query = "SELECT * FROM transactions ORDER BY date DESC"
        return execute_query(query)


def update_transaction(txn_id, **kwargs):
    """Update transaction fields based on kwargs dictionary."""
    if not kwargs:
        return
    fields = ", ".join(f"{key} = ?" for key in kwargs)
    params = list(kwargs.values())
    params.append(txn_id)
    query = f"UPDATE transactions SET {fields} WHERE txn_id = ?"
    execute_query(query, params)
    print(f"Transaction {txn_id} updated.")


def delete_transaction(txn_id):
    query = "DELETE FROM transactions WHERE txn_id = ?"
    execute_query(query, (txn_id,))
    print(f"Transaction {txn_id} deleted.")


# Similarly, you can add CRUD functions for categories and budgets

if __name__ == "__main__":
    # For initial setup run
    initialize_db()
