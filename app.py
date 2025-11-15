from engine.engine import run_full_scan
from reports.html_generator import generate_html_report
from reports.pdf_generator import generate_pdf_report


def main():
    subnet = input("Enter subnet (e.g. 192.168.1.0/24): ")

    print("\n[+] Starting full scan...\n")

    # NEW unified scanning engine
    devices = run_full_scan(subnet)

    # Generate HTML report
    html = generate_html_report(devices)
    with open("scan_report.html", "w") as f:
        f.write(html)

    # Generate PDF report
    generate_pdf_report("scan_report.pdf", html)

    print("\n[+] Reports generated:")
    print("scan_report.html")
    print("scan_report.pdf")


if __name__ == "__main__":
    main()
