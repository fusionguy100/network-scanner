from jinja2 import Template
from datetime import datetime

def generate_html_report(devices):
    high = 0
    medium = 0
    low = 0

    # Classify severity based on keyword matching
    for dev in devices:
        classified = []
        for issue in dev["issues"]:
            severity = "severity-low"

            if "vulnerable" in issue.lower() or "CVE" in issue.lower():
                severity = "severity-high"
                high += 1
            elif "risk" in issue.lower() or "deprecated" in issue.lower():
                severity = "severity-medium"
                medium += 1
            else:
                low += 1

            classified.append({"text": issue, "severity": severity})

        dev["issues"] = classified

    # Read template
    with open("reports/templates/report_template.html", "r", encoding="utf-8") as f:
        template = Template(f.read())

    return template.render(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
        device_count=len(devices),
        high_count=high,
        medium_count=medium,
        low_count=low,
        devices=devices
    )
