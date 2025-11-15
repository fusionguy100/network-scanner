import sqlite3
import json

DB_FILE = "scans.db"


def get_connection():
    """
    Creates the database file if missing.
    Ensures the 'scans' table exists with correct schema.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    create_tables(conn)
    return conn


def create_tables(conn):
    """
    Correct schema with timestamp DEFAULT CURRENT_TIMESTAMP
    """
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            devices_json TEXT NOT NULL
        );
    """)

    conn.commit()


def init_db():
    """
    Optional — ensures DB exists on start
    """
    conn = get_connection()
    conn.close()


def get_all_scans():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, timestamp FROM scans ORDER BY id DESC")
    scans = cur.fetchall()

    conn.close()
    return scans


def get_scan_by_id(scan_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM scans WHERE id = ?", (scan_id,))
    scan = cur.fetchone()

    conn.close()

    if not scan:
        return None

    return {
        "id": scan["id"],
        "timestamp": scan["timestamp"],
        "devices": json.loads(scan["devices_json"])
    }
