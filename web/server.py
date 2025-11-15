from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from engine.engine import run_full_scan
from database.db import init_db, get_connection
from database.changes import detect_changes
from reports.html_generator import generate_html_report
from reports.pdf_generator import generate_pdf_report

app = FastAPI()

app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/scan", response_class=HTMLResponse)
async def scan(request: Request, subnet: str = "192.168.0.0/24"):
    devices = run_full_scan(subnet)

    html = generate_html_report(devices)
    with open("scan_report.html", "w") as f:
        f.write(html)

    generate_pdf_report("scan_report.pdf", html)

    return templates.TemplateResponse(
        "scan.html",
        {
            "request": request,
            "devices": devices,
            "subnet": subnet
        }
    )


@app.get("/history", response_class=HTMLResponse)
async def history(request: Request):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, timestamp FROM scan_runs ORDER BY id DESC")
    scans = cur.fetchall()

    return templates.TemplateResponse("history.html",
        {"request": request, "scans": scans})


@app.get("/history/{scan_id}", response_class=HTMLResponse)
async def view_scan(request: Request, scan_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT ip, mac, vendor, os_guess, id FROM devices
        WHERE scan_id = ?
    """, (scan_id,))
    devices = cur.fetchall()

    device_list = []
    for ip, mac, vendor, os_guess, dev_id in devices:
        cur.execute("SELECT port FROM ports WHERE device_id = ?", (dev_id,))
        ports = [p[0] for p in cur.fetchall()]

        cur.execute("SELECT issue FROM issues WHERE device_id = ?", (dev_id,))
        issues = [i[0] for i in cur.fetchall()]

        device_list.append({
            "ip": ip,
            "mac": mac,
            "vendor": vendor,
            "os": os_guess,
            "ports": ports,
            "issues": issues
        })

    return templates.TemplateResponse(
        "scan.html",
        {"request": request, "devices": device_list, "subnet": "(history)"}
    )
