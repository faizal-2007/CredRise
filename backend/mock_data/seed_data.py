import sqlite3
import os
import uuid
from datetime import datetime, timedelta
import random

DB_FILE = os.path.join(os.path.dirname(__file__), '..', 'credrise.db')

def seed_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Just basic user
    user_id = "user_123"
    
    categories = ["grocery", "utility_bill", "recharge", "entertainment", "transfer_in", "transfer_out", "emi", "dining"]
    
    for i in range(50):
        tx_id = str(uuid.uuid4())
        cat = random.choice(categories)
        amt = round(random.uniform(10.0, 5000.0), 2)
        tx_time = (datetime.now() - timedelta(days=random.randint(0, 90))).isoformat()
        tx_type = "credit" if cat == "transfer_in" else "debit"
        is_late = True if cat in ["utility_bill", "emi"] and random.random() < 0.2 else False
        
        cursor.execute('''
            INSERT OR IGNORE INTO transactions (transaction_id, user_id, timestamp, amount, category, sender_receiver_id, type, status, is_late_payment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (tx_id, user_id, tx_time, amt, cat, "counterparty_abc", tx_type, "success", is_late))
        
    conn.commit()
    conn.close()
    print("Database seeded with mock transactions!")

if __name__ == "__main__":
    seed_db()
