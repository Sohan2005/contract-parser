# database.py
# Handles saving results to SQLite
import sqlite3
import json
from datetime import datetime

DB_PATH = "contracts.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # FIXED: normalized schema with proper columns
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            contract_type TEXT,
            parties TEXT,
            effective_date TEXT,
            expiry_date TEXT,
            dollar_amounts TEXT,
            key_obligations TEXT,
            termination_clause TEXT,
            governing_law TEXT,
            raw_json TEXT,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("Database initialized")

def save_result(filename: str, result: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO documents (
            filename,
            contract_type,
            parties,
            effective_date,
            expiry_date,
            dollar_amounts,
            key_obligations,
            termination_clause,
            governing_law,
            raw_json,
            created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        filename,
        result.get("contract_type"),
        json.dumps(result.get("parties", [])),
        result.get("effective_date"),
        result.get("expiry_date"),
        json.dumps(result.get("dollar_amounts", [])),
        json.dumps(result.get("key_obligations", [])),
        result.get("termination_clause"),
        result.get("governing_law"),
        json.dumps(result),
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()
    print(f"Saved to database: {filename}")

def get_all_results():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, filename, contract_type, effective_date, created_at
        FROM documents
        ORDER BY created_at DESC
    """)
    rows = cursor.fetchall()

    conn.close()
    return rows

def get_result_by_id(doc_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
    row = cursor.fetchone()

    conn.close()
    return row