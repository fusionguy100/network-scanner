from scanner.discovery import discover_hosts
from scanner.port_scan import scan_ports
from scanner.os_fingerprinting import guess_os
from scanner.vendor_lookup import lookup_vendor
from scanner.remediation import generate_recommendations

from reports.html_generator import generate_html_report
from reports.pdf_generator import generate_pdf_report

def main():
    subnet = input("Enter subnet (e.g. 192.168.1.0/24): ")

    print("\n[+] Discovering hosts...")
    hosts = discover_hosts(subnet)

    devices = []

    for host in hosts:
        ip = host["ip"]
        mac = host["mac"]

        print(f"\nScanning {ip}...")

        open_ports = scan_ports(ip)
        os_guess = guess_os(ip)
        vendor = lookup_vendor(mac)
        issues = generate_recommendations(open_ports)

        devices.append({
            "ip": ip,
            "mac": mac,
            "vendor": vendor,
            "os": os_guess,
            "open_ports": open_ports,
            "issues": issues
        })

    html = generate_html_report(devices)
    with open("scan_report.html", "w") as f:
        f.write(html)

    generate_pdf_report("scan_report.pdf", html)

    print("\n[+] Reports generated:")
    print("scan_report.html")
    print("scan_report.pdf")


if __name__ == "__main__":
    main()
