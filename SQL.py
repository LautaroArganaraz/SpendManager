import sqlite3 as sq
from pathlib import Path

import pandas as pd

DB_PATH = Path(__file__).with_name("database.db")

#This query creates the transactions table if it doesn't exist
def create_table():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        amount REAL NOT NULL,
        notes TEXT,
        category TEXT,
        date DATE
    )
    """
    with sq.connect(DB_PATH) as conn:
        conn.execute(create_table_query)

#This query will add the transaction in the database
def add_transaction(type, amount, notes, category, date):
    insert_query = """
    INSERT INTO transactions (type, amount, notes, category, date)
    VALUES (?, ?, ?, ?, ?)
    """
    with sq.connect(DB_PATH) as conn:
        conn.execute(insert_query, (type, amount, notes, category, date))

#This query gets all of the transactions
def get_transactions():
    query = """
    SELECT type AS Type, amount AS Amount, notes AS Notes, category AS Category, date AS Date
    FROM transactions
    ORDER BY id DESC
    """
    with sq.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn)

def actual_month_data():
    amd_query = """
    SELECT * FROM transactions
    WHERE date >= date('now', '-1 month')
    """
    with sq.connect(DB_PATH) as conn:
        return pd.read_sql_query(amd_query, conn)

    
def load_transactions():
    with sq.connect(DB_PATH) as conn:
        df_tr = pd.read_sql_query("SELECT * FROM transactions", conn)
    if not df_tr.empty:
        df_tr.columns = df_tr.columns.str.lower()
        if 'note' not in df_tr.columns:
            df_tr['notes'] = ''
    df_tr['notes'] = df_tr['notes'].fillna('')
    
    return df_tr