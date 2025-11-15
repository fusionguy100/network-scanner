import sqlite3
from datetime import datetime

DB_NAME = "scans.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS scan_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_id INTEGER,
            ip TEXT,
            mac TEXT,
            vendor TEXT,
            os_guess TEXT,
            FOREIGN KEY (scan_id) REFERENCES scan_runs(id)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER,
            port INTEGER,
            FOREIGN KEY (device_id) REFERENCES devices(id)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER,
            issue TEXT,
            FOREIGN KEY (device_id) REFERENCES devices(id)
        );
    """)

    conn.commit()
    conn.close()
