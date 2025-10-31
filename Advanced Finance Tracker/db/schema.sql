-- Users table (optional if multi-user support needed)
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE
);

-- Categories table for transaction classification
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_category_id INTEGER,
    FOREIGN KEY (parent_category_id) REFERENCES categories (category_id)
);

-- Transactions table storing all income, expenses, and investments
CREATE TABLE IF NOT EXISTS transactions (
    txn_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,                             -- Optional, link to users table
    date TEXT NOT NULL,                          -- ISO format date string 'YYYY-MM-DD'
    amount REAL NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('income', 'expense', 'investment')),
    category_id INTEGER,
    description TEXT,
    tags TEXT,
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (category_id) REFERENCES categories (category_id)
);

-- Budgets for tracking spending limits by category and period
CREATE TABLE IF NOT EXISTS budgets (
    budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    category_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    start_date TEXT NOT NULL,                    -- Budget valid from
    end_date TEXT NOT NULL,                      -- Budget valid till
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (category_id) REFERENCES categories (category_id)
);
