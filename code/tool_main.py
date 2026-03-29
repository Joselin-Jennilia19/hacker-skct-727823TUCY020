# student_name: Joselin Jennilia
# roll_number: 727823TUCY020
# project_name: OSINTEmailHarvester
# date: 2025-03-28

"""
OSINT Email Harvester
Extracts email addresses from publicly visible web pages
by scanning the HTML content of given URLs or domain pages.
Ethical use only — test on domains you own or have permission to scan.
"""

import re
import sys
import json
import argparse
import urllib.request
import urllib.error
from datetime import datetime
from collections import defaultdict

ROLL_NUMBER  = "727823TUCY020"
STUDENT_NAME = "Joselin Jennilia"
PROJECT_NAME = "OSINTEmailHarvester"

EMAIL_REGEX = re.compile(
    r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
)

FAKE_EMAILS = {
    "testcorp.local": [
        "admin@testcorp.local",
        "hr@testcorp.local",
        "support@testcorp.local",
        "ceo@testcorp.local",
        "info@testcorp.local",
    ],
    "demo.org": [
        "contact@demo.org",
        "webmaster@demo.org",
        "noreply@demo.org",
    ],
}

def print_banner():
    print("=" * 60)
    print(f"  OSINT Email Harvester  |  Roll No: {ROLL_NUMBER}")
    print(f"  Student   : {STUDENT_NAME}")
    print(f"  Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

def fetch_page(url):
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; OSINTHarvester/1.0)"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode(errors="replace")
    except urllib.error.HTTPError as e:
        return f"__ERROR__HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return f"__ERROR__URL {e.reason}"
    except Exception as e:
        return f"__ERROR__{e}"

def extract_emails_from_text(text):
    found = EMAIL_REGEX.findall(text)
    cleaned = set()
    for email in found:
        email = email.strip(".,;:\"'><)(][")
        if "." in email.split("@")[-1]:
            cleaned.add(email.lower())
    return cleaned

def get_candidate_urls(domain):
    prefixes = ["https://", "http://"]
    paths    = ["", "/contact", "/about", "/team", "/contact-us", "/about-us"]
    urls = []
    for prefix in prefixes:
        for path in paths:
            urls.append(f"{prefix}{domain}{path}")
        break
    return urls

def harvest_domain(domain, verbose=False):
    result = {
        "domain":    domain,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "emails":    [],
        "sources":   {},
        "pages_scanned": 0,
        "errors":    [],
        "method":    "live_scrape",
    }

    # Use synthetic data for local/fake domains
    if domain in FAKE_EMAILS:
        result["emails"]  = sorted(FAKE_EMAILS[domain])
        result["method"]  = "synthetic_dataset"
        result["sources"] = {e: f"synthetic://{domain}" for e in result["emails"]}
        result["pages_scanned"] = 1
        return result

    all_emails = set()
    urls = get_candidate_urls(domain)

    for url in urls:
        if verbose:
            print(f"  Scanning: {url}")
        content = fetch_page(url)
        if content.startswith("__ERROR__"):
            result["errors"].append(f"{url} => {content[9:]}")
            continue
        result["pages_scanned"] += 1
        found = extract_emails_from_text(content)
        # Filter to only emails belonging to this domain
        domain_emails = {e for e in found if domain in e}
        if domain_emails:
            for e in domain_emails:
                result["sources"][e] = url
        all_emails.update(domain_emails)

    result["emails"] = sorted(all_emails)
    return result

def print_result(r):
    sep = "-" * 60
    print(f"\n{sep}")
    print(f"  Domain    : {r['domain']}")
    print(f"  Scanned   : {r['timestamp']}")
    print(f"  Method    : {r['method']}")
    print(f"  Pages     : {r['pages_scanned']} scanned")
    print(sep)
    if r["emails"]:
        print(f"  Emails Found ({len(r['emails'])}):")
        for email in r["emails"]:
            src = r["sources"].get(email, "unknown")
            print(f"    {email:40s}  source: {src}")
    else:
        print("  No emails found for this domain.")
    if r["errors"]:
        print(f"  Errors ({len(r['errors'])}):")
        for err in r["errors"]:
            print(f"    {err}")
    print(sep)
    print(f"  TOTAL EMAILS HARVESTED : {len(r['emails'])}")
    print(f"{sep}\n")

def main():
    print_banner()
    parser = argparse.ArgumentParser(
        description="OSINT Email Harvester — 727823TUCY020"
    )
    parser.add_argument(
        "domains", nargs="+",
        help="Domain(s) to harvest emails from"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Save output as JSON report"
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Show each URL being scanned"
    )
    args = parser.parse_args()

    for domain in args.domains:
        print(f"\n[*] Harvesting: {domain}")
        result = harvest_domain(domain, verbose=args.verbose)
        print_result(result)
        if args.json:
            out = f"outputs/reports/{domain}_emails.json"
            with open(out, "w") as f:
                json.dump(result, f, indent=2)
            print(f"  [+] JSON saved -> {out}")

if __name__ == "__main__":
    main()
