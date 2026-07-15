import sqlite3
from config import DB_PATH


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    return conn, cursor


def init_db():
    conn, cursor = connect_db()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS businesses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                website TEXT,
                phone TEXT,
                maps_url TEXT UNIQUE NOT NULL,
                rate REAL,
                contact_page TEXT,
                emails TEXT,
                facebook TEXT,
                instagram TEXT,
                linkedin TEXT,
                youtube TEXT,
                status TEXT DEFAULT 'raw',
                lead_score INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()

    finally:
        conn.close()