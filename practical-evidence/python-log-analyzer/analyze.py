#!/usr/bin/env python3
"""Tiny web-access-log analyser.

Reads a combined-format style access log and prints a short triage summary:
top source IPs, request methods, status codes, scanner user agents and
injection-style payloads found in the query string.

Usage:
    python3 analyze.py sample_access.log
    python3 analyze.py sample_access.log --top 5
"""

import argparse
import re
import sys
from collections import Counter
from urllib.parse import unquote

LINE_RE = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) (?P<path>\S+) [^"]*" '
    r'(?P<status>\d{3}) (?P<size>\S+)'
    r'(?: "(?P<referer>[^"]*)" "(?P<ua>[^"]*)")?'
)

SUSPICIOUS_UA = [
    "sqlmap", "nikto", "nmap", "masscan", "dirbuster", "gobuster",
    "wfuzz", "hydra", "zgrab", "python-requests", "curl/", "libwww-perl",
]

# Deliberately blunt patterns: this is a triage aid, not a WAF.
PAYLOAD_PATTERNS = {
    "sql-injection": re.compile(r"(union\s+select|'\s*or\s*'1'='1|sleep\(|benchmark\()", re.I),
    "path-traversal": re.compile(r"(\.\./|%2e%2e%2f|/etc/passwd)", re.I),
    "xss": re.compile(r"(<script|%3cscript|onerror=|javascript:)", re.I),
    "command-injection": re.compile(r"(;\s*(cat|id|whoami|curl|wget)\b|\|\s*(nc|bash)\b|`)", re.I),
    "log4shell": re.compile(r"\$\{jndi:", re.I),
}


def parse(path):
    entries = []
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            m = LINE_RE.match(line.strip())
            if not m:
                continue
            e = m.groupdict()
            e["status"] = int(e["status"])
            entries.append(e)
    return entries


def bar(count, biggest, width=28):
    if biggest == 0:
        return ""
    return "#" * max(1, round(count / biggest * width))


def main():
    ap = argparse.ArgumentParser(description="Summarise a web access log.")
    ap.add_argument("logfile")
    ap.add_argument("--top", type=int, default=10, help="rows per table (default 10)")
    args = ap.parse_args()

    try:
        entries = parse(args.logfile)
    except FileNotFoundError:
        sys.exit(f"file not found: {args.logfile}")

    if not entries:
        sys.exit("no parsable lines found")

    print(f"File      : {args.logfile}")
    print(f"Requests  : {len(entries)}")
    print(f"Unique IP : {len({e['ip'] for e in entries})}")
    print()

    def table(title, counter, top=None, biggest=None):
        if not counter:
            return
        top = top or args.top
        biggest = biggest or counter.most_common(1)[0][1]
        print(title)
        for key, count in counter.most_common(top):
            print(f"  {count:>5}  {bar(count, biggest):<28}  {key}")
        print()

    table("Top source IPs", Counter(e["ip"] for e in entries))
    table("Methods", Counter(e["method"] for e in entries))
    table("Status codes", Counter(e["status"] for e in entries))

    scanners = Counter()
    for e in entries:
        ua = (e.get("ua") or "").lower()
        for needle in SUSPICIOUS_UA:
            if needle in ua:
                scanners[(e["ip"], needle)] += 1
    if scanners:
        print("Scanner-like user agents")
        for (ip, needle), count in scanners.most_common(args.top):
            print(f"  {count:>5}  {ip:<16}  {needle}")
        print()

    hits = Counter()
    examples = {}
    for e in entries:
        path = e["path"]
        decoded = unquote(path)
        for name, rx in PAYLOAD_PATTERNS.items():
            if rx.search(decoded) or rx.search(path):
                hits[(e["ip"], name)] += 1
                examples.setdefault((e["ip"], name), path[:90])
    if hits:
        print("Injection-style payloads")
        for (ip, name), count in hits.most_common(args.top):
            print(f"  {count:>5}  {name:<18}  {ip}")
            print(f"         e.g. {examples[(ip, name)]}")
        print()

    errors = sum(1 for e in entries if e["status"] >= 400)
    print(f"4xx/5xx responses : {errors} ({errors / len(entries):.0%})")
    flagged = len({e["ip"] for e in entries if any(
        n in (e.get("ua") or "").lower() for n in SUSPICIOUS_UA)}) or 0
    print(f"IPs with scanner UA: {flagged}")


if __name__ == "__main__":
    main()
