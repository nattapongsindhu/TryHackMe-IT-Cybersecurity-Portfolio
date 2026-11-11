#!/usr/bin/env python3
"""Summarise a Zeek conn.log for first-pass network triage.

Zeek writes one tab-separated row per connection and a run of "#fields" comments at
the top. This script reads that file and prints the handful of views I actually use
when a conn.log lands on my desk:

    1. volume and connection states
    2. top talkers (by connection count and by bytes sent)
    3. top destinations
    4. long-lived connections
    5. large transfers
    6. traffic to uncommon ports

The goal is to point at the rows worth reading, not to replace an analyst.

Usage:
    python zeek_conn_summary.py sample_conn.log
    python zeek_conn_summary.py conn.log --top 5
    python zeek_conn_summary.py conn.log --json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

COMMON_PORTS = {53, 80, 123, 443}

# Zeek writes '-' for missing values.
MISSING = "-"


@dataclass
class Conn:
    ts: float
    orig_h: str
    orig_p: int
    resp_h: str
    resp_p: int
    proto: str
    service: str
    duration: float
    orig_bytes: int
    resp_bytes: int
    state: str


def to_int(value: str) -> int:
    return 0 if value in (MISSING, "") else int(float(value))


def to_float(value: str) -> float:
    return 0.0 if value in (MISSING, "") else float(value)


def read_conn_log(path: Path) -> tuple[list[Conn], int, int]:
    """Return (connections, skipped_rows, header_field_count)."""
    fields = None
    conns: list[Conn] = []
    skipped = 0

    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if not line:
                continue
            if line.startswith("#"):
                if line.startswith("#fields"):
                    fields = line.split("\t")[1:]
                continue
            if fields is None:
                skipped += 1
                continue
            parts = line.split("\t")
            if len(parts) < 11:
                skipped += 1
                continue
            row = dict(zip(fields, parts))
            try:
                conns.append(
                    Conn(
                        ts=to_float(row.get("ts", "0")),
                        orig_h=row.get("id.orig_h", "?"),
                        orig_p=to_int(row.get("id.orig_p", "0")),
                        resp_h=row.get("id.resp_h", "?"),
                        resp_p=to_int(row.get("id.resp_p", "0")),
                        proto=row.get("proto", "?"),
                        service=row.get("service", MISSING),
                        duration=to_float(row.get("duration", "0")),
                        orig_bytes=to_int(row.get("orig_bytes", "0")),
                        resp_bytes=to_int(row.get("resp_bytes", "0")),
                        state=row.get("conn_state", "?"),
                    )
                )
            except ValueError:
                skipped += 1

    return conns, skipped, len(fields or [])


def human_bytes(value: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1024 or unit == "GB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{value} B"
        value /= 1024.0
    return f"{value:.1f} GB"


def summarise(conns: list[Conn], top: int) -> dict:
    sources = Counter(c.orig_h for c in conns)
    dests = Counter(c.resp_h for c in conns)
    states = Counter(c.state for c in conns)

    sent: defaultdict[str, int] = defaultdict(int)
    for conn in conns:
        sent[conn.orig_h] += conn.orig_bytes

    odd_ports = Counter(
        c.resp_p for c in conns if c.resp_p not in COMMON_PORTS and c.resp_p < 1024
    )

    long_conns = sorted(conns, key=lambda c: c.duration, reverse=True)[:top]
    big_transfers = sorted(conns, key=lambda c: c.orig_bytes + c.resp_bytes, reverse=True)[:top]

    return {
        "connections": len(conns),
        "unique_sources": len(sources),
        "unique_destinations": len(dests),
        "states": states.most_common(),
        "top_sources": sources.most_common(top),
        "top_senders_bytes": sorted(sent.items(), key=lambda kv: -kv[1])[:top],
        "top_destinations": dests.most_common(top),
        "uncommon_ports": odd_ports.most_common(top),
        "longest": [
            {
                "source": c.orig_h,
                "destination": f"{c.resp_h}:{c.resp_p}",
                "service": c.service,
                "duration_s": round(c.duration, 1),
                "sent": human_bytes(c.orig_bytes),
            }
            for c in long_conns
        ],
        "largest": [
            {
                "source": c.orig_h,
                "destination": f"{c.resp_h}:{c.resp_p}",
                "service": c.service,
                "total": human_bytes(c.orig_bytes + c.resp_bytes),
            }
            for c in big_transfers
        ],
    }


def print_report(data: dict, top: int) -> None:
    line = "=" * 68
    print(line)
    print(f" ZEEK conn.log TRIAGE   {data['connections']} connections")
    print(line)

    print("\n[1] VOLUME")
    print(f"    connections        : {data['connections']}")
    print(f"    unique sources     : {data['unique_sources']}")
    print(f"    unique destinations: {data['unique_destinations']}")
    if data["states"]:
        print("    connection states  : " + ", ".join(f"{s}={n}" for s, n in data["states"][:5]))

    print(f"\n[2] TOP {top} TALKERS (by connections)")
    if data["top_sources"]:
        biggest = data["top_sources"][0][1]
        for host, count in data["top_sources"]:
            bars = "#" * max(1, round(count / biggest * 24))
            print(f"    {count:>5}  {bars:<24}  {host}")

    print(f"\n[3] TOP {top} SENDERS (by bytes)")
    for host, total in data["top_senders_bytes"]:
        print(f"    {human_bytes(total):>10}  {host}")

    print(f"\n[4] TOP {top} DESTINATIONS")
    for host, count in data["top_destinations"]:
        print(f"    {count:>5}  {host}")

    print(f"\n[5] UNCOMMON LOW PORTS (not 53/80/123/443)")
    if data["uncommon_ports"]:
        for port, count in data["uncommon_ports"]:
            print(f"    {count:>5}  port {port}")
    else:
        print("    none")

    print(f"\n[6] LONGEST CONNECTIONS")
    for row in data["longest"]:
        print(f"    {row['duration_s']:>8}s  {row['source']:<15} -> {row['destination']:<22} "
              f"{row['service']:<8} sent {row['sent']}")

    print(f"\n[7] LARGEST TRANSFERS")
    for row in data["largest"]:
        print(f"    {row['total']:>10}  {row['source']:<15} -> {row['destination']:<22} {row['service']}")

    print("\n" + line)
    print(" Read order: [5] odd ports, then [7] big transfers, then [2] the loudest host.")
    print(line)


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarise a Zeek conn.log.")
    parser.add_argument("logfile", type=Path)
    parser.add_argument("--top", type=int, default=8)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.logfile.exists():
        print(f"File not found: {args.logfile}", file=sys.stderr)
        return 1

    conns, skipped, field_count = read_conn_log(args.logfile)
    if not conns:
        print("No connection rows found.", file=sys.stderr)
        return 1

    data = summarise(conns, args.top)
    data["skipped_rows"] = skipped
    data["header_fields"] = field_count

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print_report(data, args.top)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
