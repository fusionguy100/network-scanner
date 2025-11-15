Network Scanner & Security Dashboard

A lightweight network reconnaissance and monitoring tool built with Python, FastAPI, SQLite, and multithreaded scanning.
It provides fast host discovery, port scanning, OS fingerprinting, vulnerability checks, and a full web dashboard with scan history.

Features
Network Discovery

Multi-threaded ICMP ping sweep

Detects active hosts across a subnet

High-performance scanning using thread pools

Port Scanning

Fast TCP SYN-style port scan

Configurable port list

Open port enumeration per host

OS Fingerprinting

Lightweight fingerprinting based on TTL and open ports

Vendor lookup via MAC (optional)

Vulnerability Detection

Basic rule-driven vulnerability checks

Flags weak services, unsafe ports, and exposed attack surface

Web Dashboard (FastAPI)

Real-time scan results

Device table with IP, OS, ports, and issues

Severity summary (high, medium, low)

Scan history stored in SQLite

Change detection: new devices, removed devices, port changes

Reporting

HTML report generation

PDF report generation (optional, depending on environment)

Tech Stack
Backend

Python 3

FastAPI

SQLite

Multithreading and asyncio

Custom scanning engine (ping, ports, OS, vuln rules)

Frontend

HTML templates (Jinja2)

JavaScript (fetch API)

Chart.js (statistics and graphs)

Bootstrap-style CSS (custom)
