import asyncio

from engine.fast_ping_scan import fast_ping_scan
from engine.fast_port_scan import fast_port_scan
from scanner.os_fingerprinting import guess_os
from scanner.vendor_lookup import lookup_vendor
from scanner.remediation import generate_recommendations
from vuln.vulnerability_scanner import scan_vulnerabilities

from database.models import save_scan
from database.db import init_db
from database.changes import detect_changes


async def run_full_scan_async(subnet):
    print("[+] Running fast network scan...")
    active_ips = fast_ping_scan(subnet)

    devices = []

    for ip in active_ips:
        print(f"\n[+] Scanning host: {ip}")

        vendor = "Unknown"

        # PORT SCANNING — supports async or sync
        future = fast_port_scan(ip)

        if asyncio.isfuture(future):
            open_ports = await future
        else:
            open_ports = future

        # OS fingerprint
        os_guess = guess_os(ip)

        # vulnerability + basic issues
        basic_issues = generate_recommendations(open_ports)
        vuln_issues = scan_vulnerabilities(ip, open_ports)
        issues = basic_issues + vuln_issues

        devices.append({
            "ip": ip,
            "mac": "Unknown",
            "vendor": vendor,
            "os": os_guess,
            "open_ports": open_ports,
            "issues": issues
        })

    # Save results AFTER scanning is complete
    init_db()
    scan_id = save_scan(devices)
    print(f"[+] Scan saved with ID {scan_id}")

    # Detect changes
    changes = detect_changes()

    if changes["first_run"]:
        print("[+] First scan — no comparison data yet.")
    else:
        print("\n[+] Changes detected since last scan:")

        if changes["new_devices"]:
            print("  New devices:")
            for ip in changes["new_devices"]:
                print(f"    + {ip}")

        if changes["removed_devices"]:
            print("  Removed devices:")
            for ip in changes["removed_devices"]:
                print(f"    - {ip}")

        if changes["port_changes"]:
            print("  Port changes:")
            for entry in changes["port_changes"]:
                print(f"    {entry['ip']}: opened={entry['opened']} closed={entry['closed']}")

    return devices


def run_full_scan(subnet):
    """
    Wrapper so CLI can run synchronously,
    and FastAPI can run asynchronously.
    """
    try:
        loop = asyncio.get_running_loop()
        # FastAPI environment → return coroutine
        return loop.create_task(run_full_scan_async(subnet))
    except RuntimeError:
        # CLI environment → run blocking
        return asyncio.run(run_full_scan_async(subnet))
