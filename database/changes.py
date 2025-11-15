from database.db import get_connection


def get_last_two_scans():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM scan_runs ORDER BY id DESC LIMIT 2")
    rows = cur.fetchall()

    conn.close()

    if len(rows) < 2:
        return None, None

    return rows[1][0], rows[0][0]   # (previous, latest)


def get_devices_for_scan(scan_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, ip FROM devices WHERE scan_id = ?", (scan_id,))
    devices = cur.fetchall()

    conn.close()
    return devices


def get_ports_for_device(device_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT port FROM ports WHERE device_id = ?", (device_id,))
    ports = [row[0] for row in cur.fetchall()]

    conn.close()
    return ports


def detect_changes():
    prev_scan, latest_scan = get_last_two_scans()

    if not prev_scan:
        return {"first_run": True}

    prev_devices = get_devices_for_scan(prev_scan)
    latest_devices = get_devices_for_scan(latest_scan)

    prev_ips = {d[1]: d[0] for d in prev_devices}
    latest_ips = {d[1]: d[0] for d in latest_devices}

    # New devices
    new_devices = [ip for ip in latest_ips if ip not in prev_ips]

    # Removed devices
    removed_devices = [ip for ip in prev_ips if ip not in latest_ips]

    # Port changes
    port_changes = []

    for ip, dev_id in latest_ips.items():
        if ip in prev_ips:
            old_dev_id = prev_ips[ip]
            old_ports = set(get_ports_for_device(old_dev_id))
            new_ports = set(get_ports_for_device(dev_id))

            opened = list(new_ports - old_ports)
            closed = list(old_ports - new_ports)

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
