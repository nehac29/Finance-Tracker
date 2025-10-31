import re
from datetime import datetime


def validate_date(date_text, date_format="%Y-%m-%d"):
    """Validate date string format."""
    try:
        datetime.strptime(date_text, date_format)
        return True
    except ValueError:
        return False


def sanitize_string(s):
    """Trim whitespace and remove problematic characters."""
    if not s or not isinstance(s, str):
        return None
    s = s.strip()
    s = re.sub(r'[^\w\s,-]', '', s)  # Remove special chars except comma, dash
    return s if s else None


def parse_tags(tag_string):
    """Parse comma-separated tags into a cleaned list."""
    if not tag_string or not isinstance(tag_string, str):
        return []
    tags = [sanitize_string(t) for t in tag_string.split(",")]
    return [t for t in tags if t]  # Filter out empty strings


def format_amount(amount):
    """Ensure amount is float rounded to 2 decimal places."""
    try:
        return round(float(amount), 2)
    except (ValueError, TypeError):
        return None


def normalize_transaction_type(txn_type):
    """Normalize transaction type string."""
    if not txn_type or not isinstance(txn_type, str):
        return None
    txn_type = txn_type.strip().lower()
    valid_types = ['income', 'expense', 'investment']
    return txn_type if txn_type in valid_types else None
