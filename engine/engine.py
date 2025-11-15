from engine.fast_ping_scan import fast_ping_scan
from engine.fast_port_scan import fast_port_scan
from scanner.os_fingerprinting import guess_os
from scanner.vendor_lookup import lookup_vendor
from scanner.remediation import generate_recommendations


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
        issues = generate_recommendations(open_ports)

        devices.append({
            "ip": ip,
            "mac": "Unknown",
            "vendor": vendor,
            "os": os_guess,
            "open_ports": open_ports,
            "issues": issues
        })

    return devices
