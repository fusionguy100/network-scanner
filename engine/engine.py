from engine.fast_ping_scan import fast_ping_scan
from engine.fast_port_scan import fast_port_scan
from scanner.os_fingerprinting import guess_os
from scanner.vendor_lookup import lookup_vendor
from scanner.remediation import generate_recommendations
from database.models import save_scan
from database.db import init_db
from database.changes import detect_changes
from vuln.vulnerability_scanner import scan_vulnerabilities


def run_full_scan(subnet):
    print("[+] Running fast network scan...")
    active_ips = fast_ping_scan(subnet)

    devices = []

    for ip in active_ips:
        print(f"\n[+] Scanning host: {ip}")

        try:
            vendor = lookup_vendor("00:00:00:00:00:00")  # placeholder
        except:
            vendor = "Unknown"

        # fast port scanning
        open_ports = fast_port_scan(ip)

        # OS fingerprinting
        os_guess = guess_os(ip)

        # remediation
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

        # initialize DB if needed
        init_db()

        scan_id = save_scan(devices)
        print(f"[+] Scan saved with ID {scan_id}")

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
