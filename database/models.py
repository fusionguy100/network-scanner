import os
import sqlite3
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, "scans.db")


def save_scan(devices):
    """
    Saves a full scan (list of device dictionaries) into the database.
    Returns the scan ID.
    """
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    # Serialize device list to JSON
    devices_json = json.dumps(devices)

    cur.execute("""
        INSERT INTO scans (devices_json)
        VALUES (?)
    """, (devices_json,))

    con.commit()
    scan_id = cur.lastrowid
    con.close()

    return scan_id


def get_scan_by_id(scan_id):
    """
    Load a single saved scan from DB by ID.
    """
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    cur.execute("SELECT id, timestamp, devices_json FROM scans WHERE id = ?", (scan_id,))
    row = cur.fetchone()
    con.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "timestamp": row[1],
        "devices": json.loads(row[2])
    }


def get_all_scans():
    """
    Returns a list of all scans with only metadata (no devices).
    """
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    cur.execute("SELECT id, timestamp FROM scans ORDER BY id DESC")
    rows = cur.fetchall()
    con.close()

    scans = []
    for r in rows:
        scans.append({
            "id": r[0],
            "timestamp": r[1]
        })

    return scans
