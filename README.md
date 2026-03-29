# OSINT Email Harvester
**Roll No:** 727823TUCY020 | **Student:** Joselin Jennilia
**Category:** OSINT / Cybersecurity
**Repo:** hacker-skct-727823TUCY020

---

## What This Tool Does
A Python tool that harvests publicly visible email addresses
from domain names by scanning web pages and extracting
email patterns from HTML content.
All testing is done on synthetic or publicly permitted domains only.

---

## Lab Environment
- OS: Kali Linux (VirtualBox VM)
- Python: 3.13
- All testing done on synthetic test domains
- No real private data was accessed at any point

---

## Setup
```bash
git clone https://github.com/YOUR_USERNAME/hacker-skct-727823TUCY020.git
cd hacker-skct-727823TUCY020
pip3 install -r requirements.txt --break-system-packages
```

---

## Usage

### Harvest a single domain
```bash
python3 code/tool_main.py testcorp.local
```

### Harvest multiple domains
```bash
python3 code/tool_main.py testcorp.local demo.org
```

### Verbose mode and save JSON
```bash
python3 code/tool_main.py testcorp.local --verbose --json
```

### Run full pipeline
```bash
python3 code/setup_lab.py
python3 code/run_tool.py
python3 code/analyze_results.py
```

---

## Test Results

| # | Domain | Emails Found | Method | Verdict |
|---|--------|-------------|--------|---------|
| 1 | testcorp.local | 5 | synthetic | 5 emails harvested |
| 2 | demo.org | 3 | synthetic | 3 emails harvested |
| 3 | both domains --verbose | 8 | synthetic | multi-domain scan |

---

## Project Structure
```
SKCT_727823TUCY020_OSINTEmailHarvester/
├── code/
│   ├── tool_main.py
│   ├── setup_lab.py
│   ├── run_tool.py
│   └── analyze_results.py
├── test_samples/
├── outputs/
├── screenshots/
├── notebooks/
├── report/
├── pipeline_727823TUCY020.yml
├── requirements.txt
└── README.md
```

---

## Ethical Notice
All testing was done on synthetic domains created by the student
inside an isolated VirtualBox VM.
No real private email addresses were harvested or stored.
This tool is for educational purposes only.
