# utils/tracker.py

import csv
from datetime import datetime
from pathlib import Path

LOG_PATH = Path("applications.csv")

def init_log():
    if not LOG_PATH.exists():
        with open(LOG_PATH, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "job_url", "company", "status", "notes"])

def log_application(job_url: str, company: str, status: str, notes: str = ""):
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.utcnow().isoformat(),
            job_url,
            company,
            status,
            notes
        ])
