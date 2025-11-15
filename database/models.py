from database.db import get_connection
from datetime import datetime


def save_scan(devices):
    conn = get_connection()
    cur = conn.cursor()

    # Create new scan_run entry
    timestamp = datetime.now().isoformat()
    cur.execute("INSERT INTO scan_runs (timestamp) VALUES (?)", (timestamp,))
    scan_id = cur.lastrowid

    for dev in devices:
        cur.execute("""
            INSERT INTO devices (scan_id, ip, mac, vendor, os_guess)
            VALUES (?, ?, ?, ?, ?)
        """, (scan_id, dev["ip"], dev["mac"], dev["vendor"], dev["os"]))

        device_id = cur.lastrowid

        # Save ports
        for port in dev["open_ports"]:
            cur.execute("INSERT INTO ports (device_id, port) VALUES (?, ?)", (device_id, port))

        # Save issues
        for issue in dev["issues"]:
            cur.execute("INSERT INTO issues (device_id, issue) VALUES (?, ?)", (device_id, issue))

    conn.commit()
    conn.close()

    return scan_id
