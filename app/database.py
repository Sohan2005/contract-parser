# database.py
# Handles saving results to SQLite
import sqlite3
import json
from datetime import datetime

DB_PATH = "contracts.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # BAD: storing everything as one json blob
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            raw_json TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()

def save_result(filename: str, result: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO documents (filename, raw_json, created_at)
        VALUES (?, ?, ?)
    """, (
        filename,
        json.dumps(result),
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()
    print(f"Saved to database: {filename}")

def get_all_results():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM documents")
    rows = cursor.fetchall()

    conn.close()
    return rows