# Joselin Jennilia | 727823TUCY020
# student_name: Joselin Jennilia
# roll_number: 727823TUCY020
# project_name: OSINTEmailHarvester
# date: 2025-03-28

import os, sys, subprocess
from datetime import datetime

ROLL_NUMBER = "727823TUCY020"

print(f"ROLL_NUMBER : {ROLL_NUMBER}")
print(f"TIMESTAMP   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"SCRIPT      : setup_lab.py — Stage 1 (Lab Setup)")
print("-" * 55)

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, "..")

DIRS = [
    "test_samples", "outputs/reports",
    "outputs/logs", "screenshots",
    "report", "notebooks"
]

for d in DIRS:
    path = os.path.join(ROOT, d)
    os.makedirs(path, exist_ok=True)
    log(f"Directory OK : {d}")

log("Installing dependencies...")
try:
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install",
         "requests", "beautifulsoup4",
         "--quiet", "--break-system-packages"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    log("pip install  : OK (requests, beautifulsoup4)")
except Exception as e:
    log(f"pip warning  : {e}")

# Write target domains file
SAMPLES = os.path.join(ROOT, "test_samples")

targets = os.path.join(SAMPLES, "targets.txt")
with open(targets, "w") as f:
    f.write("testcorp.local\n")
    f.write("demo.org\n")
log(f"Targets file : {targets}")

# Write synthetic email dataset
dataset = os.path.join(SAMPLES, "synthetic_emails.txt")
with open(dataset, "w") as f:
    f.write("# Synthetic email dataset for testing\n")
    f.write("# roll_number: 727823TUCY020\n\n")
    f.write("testcorp.local: admin@testcorp.local, hr@testcorp.local, ")
    f.write("support@testcorp.local, ceo@testcorp.local, info@testcorp.local\n")
    f.write("demo.org: contact@demo.org, webmaster@demo.org, noreply@demo.org\n")
log(f"Dataset file : {dataset}")

print("-" * 55)
log(f"Stage 1 COMPLETE — ROLL_NUMBER : {ROLL_NUMBER}")
