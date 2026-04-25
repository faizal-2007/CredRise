import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), 'credrise.db')

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            user_id TEXT,
            timestamp TEXT,
            amount REAL,
            category TEXT,
            sender_receiver_id TEXT,
            type TEXT,
            status TEXT,
            is_late_payment BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()
