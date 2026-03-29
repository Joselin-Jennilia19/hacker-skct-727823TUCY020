# Joselin Jennilia | 727823TUCY020
# student_name: Joselin Jennilia
# roll_number: 727823TUCY020
# project_name: OSINTEmailHarvester
# date: 2025-03-28

import os, sys, json, csv
from datetime import datetime

ROLL_NUMBER = "727823TUCY020"

print(f"ROLL_NUMBER : {ROLL_NUMBER}")
print(f"TIMESTAMP   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"SCRIPT      : run_tool.py — Stage 2 (Tool Execution)")
print("-" * 55)

BASE    = os.path.dirname(os.path.abspath(__file__))
ROOT    = os.path.join(BASE, "..")
SAMPLES = os.path.join(ROOT, "test_samples")
OUTDIR  = os.path.join(ROOT, "outputs", "reports")
LOGDIR  = os.path.join(ROOT, "outputs", "logs")

os.makedirs(OUTDIR, exist_ok=True)
os.makedirs(LOGDIR, exist_ok=True)

sys.path.insert(0, BASE)
from tool_main import harvest_domain, print_result

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

targets_file = os.path.join(SAMPLES, "targets.txt")
if not os.path.isfile(targets_file):
    log("ERROR: targets.txt not found. Run setup_lab.py first.")
    sys.exit(1)

with open(targets_file) as f:
    domains = [line.strip() for line in f if line.strip()
               and not line.startswith("#")]

log(f"Found {len(domains)} target domain(s)")

all_results = []

for i, domain in enumerate(domains, 1):
    log(f"[{i}/{len(domains)}] Harvesting: {domain}")
    result = harvest_domain(domain, verbose=True)
    print_result(result)
    all_results.append(result)

    jname = f"{domain.replace('.', '_')}_emails.json"
    jpath = os.path.join(OUTDIR, jname)
    with open(jpath, "w") as jf:
        json.dump(result, jf, indent=2)
    log(f"  JSON saved -> {jname}")

combined = os.path.join(OUTDIR, "all_results.json")
with open(combined, "w") as cf:
    json.dump(all_results, cf, indent=2)
log(f"Combined JSON -> all_results.json")

csv_path = os.path.join(OUTDIR, "summary.csv")
with open(csv_path, "w", newline="") as cf:
    writer = csv.writer(cf)
    writer.writerow(["domain", "emails_found", "pages_scanned",
                     "method", "timestamp"])
    for r in all_results:
        writer.writerow([
            r["domain"], len(r["emails"]),
            r["pages_scanned"], r["method"], r["timestamp"]
        ])
log(f"CSV saved     -> summary.csv")

logfile = os.path.join(LOGDIR, "run_tool.log")
with open(logfile, "w") as lf:
    lf.write(f"roll_number : {ROLL_NUMBER}\n")
    lf.write(f"timestamp   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lf.write("=" * 55 + "\n")
    for r in all_results:
        lf.write(
            f"{r['timestamp']} | {r['domain']:25s} | "
            f"emails={len(r['emails']):3d} | method={r['method']}\n"
        )
log(f"Log saved     -> run_tool.log")

print("-" * 55)
log(f"Stage 2 COMPLETE — harvested {len(all_results)} domain(s)")
log(f"ROLL_NUMBER : {ROLL_NUMBER}")
