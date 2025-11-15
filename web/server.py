import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Import your scanning engine
from engine.engine import run_full_scan

app = FastAPI()

# Serve static files (CSS, JS)
STATIC_DIR = os.path.join("web", "static")
TEMPLATE_DIR = os.path.join("web", "templates")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Jinja2 Template Loader
templates = Jinja2Templates(directory=TEMPLATE_DIR)


# ---------------------------------------------------------
#  HOME PAGE (dashboard)
# ---------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


# ---------------------------------------------------------
#  RUN SCAN API — triggered from Dashboard button
# ---------------------------------------------------------
@app.get("/scan", response_class=JSONResponse)
def scan(subnet: str = "192.168.0.0/24"):
    """
    Example:
      GET /scan?subnet=192.168.0.0/24
    """
    print(f"[+] Running full scan on {subnet}")

    devices = run_full_scan(subnet)

    return {"status": "ok", "count": len(devices), "devices": devices}


# ---------------------------------------------------------
#  API: DEVICES (dashboard table loads from here)
# ---------------------------------------------------------
@app.get("/api/devices", response_class=JSONResponse)
def api_devices(subnet: str = "192.168.0.0/24"):
    devices = run_full_scan(subnet)
    return {"devices": devices}


# ---------------------------------------------------------
#  API: SUMMARY (open ports, OS distribution, issues, etc.)
# ---------------------------------------------------------
@app.get("/api/summary", response_class=JSONResponse)
def api_summary(subnet: str = "192.168.0.0/24"):
    devices = run_full_scan(subnet)

    summary = {
        "device_count": len(devices),
        "os_counts": {},
        "total_open_ports": 0,
        "issue_count": 0
    }

    for d in devices:
        os_name = d["os"]
        summary["os_counts"][os_name] = summary["os_counts"].get(os_name, 0) + 1
        summary["total_open_ports"] += len(d["open_ports"])
        summary["issue_count"] += len(d["issues"])

    return summary


# ---------------------------------------------------------
#  HISTORY PAGE (saved scans)
# ---------------------------------------------------------
@app.get("/history", response_class=HTMLResponse)
def history_page(request: Request):
    return templates.TemplateResponse("history.html", {"request": request})


# ---------------------------------------------------------
#  INDIVIDUAL SCAN REPORT PAGE
# ---------------------------------------------------------
@app.get("/scan-report", response_class=HTMLResponse)
def scan_report(request: Request):
    return templates.TemplateResponse("scan.html", {"request": request})


# ---------------------------------------------------------
#  HEALTH CHECK (optional)
# ---------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "running"}
