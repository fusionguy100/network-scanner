import os
import sys
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Database
from database.db import init_db, get_all_scans, get_scan_by_id
from database.changes import detect_changes

# Scanning engine
from engine.engine import run_full_scan

# ---------------------------------------------------------
#  FIX FOR PYINSTALLER (templates/static paths)
# ---------------------------------------------------------
if getattr(sys, 'frozen', False):
    # Running from .exe
    BASE_DIR = sys._MEIPASS
else:
    # Running from source
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

# ---------------------------------------------------------

app = FastAPI()

# Initialize DB on startup
init_db()

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Template engine
templates = Jinja2Templates(directory=TEMPLATE_DIR)


# ---------------------------------------------------------
#  HOME PAGE (Dashboard) — DOES NOT TRIGGER SCAN
# ---------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


# ---------------------------------------------------------
#  RUN SCAN — ONLY runs when user clicks Scan button
# ---------------------------------------------------------
@app.get("/scan", response_class=JSONResponse)
def scan(subnet: str = "192.168.0.0/24"):
    print(f"[+] Running full scan on {subnet}")
    devices = run_full_scan(subnet)
    return {"status": "ok", "count": len(devices), "devices": devices}


# ---------------------------------------------------------
#  API: DEVICES — Returns LAST SAVED scan
# ---------------------------------------------------------
@app.get("/api/devices", response_class=JSONResponse)
def api_devices():
    scans = get_all_scans()
    if not scans:
        return {"devices": []}

    last_scan_id = scans[0]["id"]
    scan = get_scan_by_id(last_scan_id)
    return {"devices": scan["devices"]}


# ---------------------------------------------------------
#  API: SUMMARY — Based on LAST scan
# ---------------------------------------------------------
@app.get("/api/summary", response_class=JSONResponse)
def api_summary():
    scans = get_all_scans()
    if not scans:
        return {
            "total_devices": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }

    last_scan_id = scans[0]["id"]
    scan = get_scan_by_id(last_scan_id)
    devices = scan["devices"]

    high = medium = low = 0

    for d in devices:
        for issue in d["issues"]:
            sev = issue.get("severity", "").lower()
            if sev == "high":
                high += 1
            elif sev == "medium":
                medium += 1
            elif sev == "low":
                low += 1

    return {
        "total_devices": len(devices),
        "high": high,
        "medium": medium,
        "low": low
    }


# ---------------------------------------------------------
#  HISTORY LIST PAGE
# ---------------------------------------------------------
@app.get("/history", response_class=HTMLResponse)
def history_page(request: Request):
    scans = get_all_scans()
    return templates.TemplateResponse("history.html", {
        "request": request,
        "scans": scans
    })


# ---------------------------------------------------------
#  INDIVIDUAL SCAN DETAIL PAGE
# ---------------------------------------------------------
@app.get("/history/{scan_id}", response_class=HTMLResponse)
def history_detail(scan_id: int, request: Request):
    scan = get_scan_by_id(scan_id)
    return templates.TemplateResponse("scan_detail.html", {
        "request": request,
        "scan": scan
    })


# ---------------------------------------------------------
#  CHANGES DASHBOARD
# ---------------------------------------------------------
@app.get("/changes", response_class=HTMLResponse)
def changes_page(request: Request):
    return templates.TemplateResponse("changes.html", {
        "request": request
    })


@app.get("/api/changes", response_class=JSONResponse)
def api_changes():
    return detect_changes()


# ---------------------------------------------------------
#  HEALTH CHECK
# ---------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "running"}
