# Joselin Jennilia | 727823TUCY020
# student_name: Joselin Jennilia
# roll_number: 727823TUCY020
# project_name: OSINTEmailHarvester
# date: 2025-03-28

import os, json
from datetime import datetime

ROLL_NUMBER = "727823TUCY020"

print(f"ROLL_NUMBER : {ROLL_NUMBER}")
print(f"TIMESTAMP   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"SCRIPT      : analyze_results.py — Stage 3 (Analysis)")
print("-" * 65)

BASE   = os.path.dirname(os.path.abspath(__file__))
ROOT   = os.path.join(BASE, "..")
OUTDIR = os.path.join(ROOT, "outputs", "reports")

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

combined = os.path.join(OUTDIR, "all_results.json")
if not os.path.isfile(combined):
    log("ERROR: all_results.json not found. Run run_tool.py first.")
    raise SystemExit(1)

with open(combined) as f:
    results = json.load(f)

log(f"Loaded {len(results)} result(s)")

print("\n" + "=" * 70)
print(f"{'DOMAIN':25s} {'EMAILS':>8} {'PAGES':>7} {'METHOD':>18} TIMESTAMP")
print("=" * 70)
for r in results:
    print(f"{r['domain']:25s} {len(r['emails']):>8} "
          f"{r['pages_scanned']:>7} {r['method']:>18} {r['timestamp']}")
print("=" * 70)

total_emails  = sum(len(r["emails"]) for r in results)
total_domains = len(results)
all_emails    = []
for r in results:
    all_emails.extend(r["emails"])

print(f"\n-- Summary Statistics --")
print(f"  Total domains scanned : {total_domains}")
print(f"  Total emails found    : {total_emails}")
print(f"  Avg emails per domain : {total_emails/total_domains:.1f}")
print(f"  Unique emails total   : {len(set(all_emails))}")

print(f"\n-- All Harvested Emails --")
for r in results:
    print(f"\n  [{r['domain']}]")
    if r["emails"]:
        for email in r["emails"]:
            print(f"    {email}")
    else:
        print(f"    No emails found")

print("-" * 65)
log(f"Stage 3 COMPLETE — ROLL_NUMBER : {ROLL_NUMBER}")
