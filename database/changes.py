import os
import sqlite3
import json

# Load DB file path (same as db.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, "scans.db")


# Internal helper
def _get_last_two_scans():
    """Returns the last 2 scans from DB, newest first."""
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    cur.execute("SELECT id, devices_json FROM scans ORDER BY id DESC LIMIT 2")
    rows = cur.fetchall()
    con.close()

    return rows


def detect_changes():
    """
    Compares the last scan vs the previous scan and detects:
      - new devices
      - removed devices
      - opened ports
      - closed ports
    """
    rows = _get_last_two_scans()

    if len(rows) < 2:
        return {
            "first_run": True,
            "new_devices": [],
            "removed_devices": [],
            "port_changes": []
        }

    latest_id, latest_json = rows[0]
    prev_id, prev_json = rows[1]

    latest = json.loads(latest_json)
    prev = json.loads(prev_json)

    latest_ips = {d["ip"]: d for d in latest}
    prev_ips = {d["ip"]: d for d in prev}

    # ------------------------------------
    # Detect new & removed devices
    # ------------------------------------
    new_devices = [ip for ip in latest_ips if ip not in prev_ips]
    removed_devices = [ip for ip in prev_ips if ip not in latest_ips]

    # ------------------------------------
    # Detect port changes
    # ------------------------------------
    port_changes = []

    for ip in latest_ips:
        if ip in prev_ips:
            latest_ports = set(latest_ips[ip]["open_ports"])
            prev_ports = set(prev_ips[ip]["open_ports"])

            opened = list(latest_ports - prev_ports)
            closed = list(prev_ports - latest_ports)

            if opened or closed:
                port_changes.append({
                    "ip": ip,
                    "opened": opened,
                    "closed": closed
                })

    return {
        "first_run": False,
        "new_devices": new_devices,
        "removed_devices": removed_devices,
        "port_changes": port_changes
    }
