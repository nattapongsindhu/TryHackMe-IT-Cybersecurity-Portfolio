# 6. Practical Evidence

Six investigations and two supporting artefacts. Each entry states **scope → method → finding →
outcome**, which is the same structure used in the full reports.

> The detailed reports are kept in a private working repository. They contain room answers and flags
> for labs that are still active, so they are deliberately not published here. What follows is the
> defensible summary: what the investigation covered and what it concluded.

## Overview

| # | Investigation | Type | Tools | Demonstrated skill |
| :---: | :--- | :--- | :--- | :--- |
| 1 | Network traffic analysis | Blue team | Wireshark | Packet-level reconstruction of an incident |
| 2 | SIEM alert investigation | Blue team | Splunk, SPL | Log correlation, alert triage, verdict writing |
| 3 | Windows endpoint investigation | Blue team | Event Viewer, Sysmon | Process lineage and persistence analysis |
| 4 | NIDS rule analysis | Blue team | Snort, Zeek | Detection engineering and false-positive reasoning |
| 5 | Linux privilege escalation | Red team | Nmap, Linux CLI | Attacker perspective on a Linux host |
| 6 | Windows SMB exploitation | Red team | Nmap, Metasploit-adjacent tooling | Attacker perspective on an unpatched SMB service |

---

## Report 1 — Network traffic analysis

**Scope:** a capture provided as part of a traffic-analysis lab.
**Method:** protocol statistics first, then conversation-level review, then stream reconstruction for
the sessions that carried data.
**Finding:** the capture showed a multi-stage exchange in which an initial request led to a second
download from an unrelated host — the classic "first contact is not the payload" pattern.
**Outcome:** produced a timeline of the exchange and a list of indicators that would survive a
rebuild of the payload (behaviour and infrastructure, not file hashes).

## Report 2 — SIEM alert investigation

**Scope:** a Splunk dataset of roughly twelve thousand events from a simulated incident.
**Method:** narrowed by index and time, built a process-and-network timeline, then correlated the
suspicious account activity against authentication events.
**Finding:** a homoglyph display name was used to impersonate a legitimate account, followed by a
command-and-control stager execution. The account naming trick is what made the initial alert look
benign.
**Outcome:** verdict of true positive, a written close-out note, and a shortlist of detections that
would have caught the stager earlier.

## Report 3 — Windows endpoint investigation

**Scope:** a Windows host compromised through a document-based exploit chain.
**Method:** process creation telemetry first (parent/child relationships), then service and scheduled
task persistence, then network connections from the suspicious process tree.
**Finding:** the chain moved from an office document handler to a scripting interpreter, then to a
tunnelling binary, then to a privilege-escalation step. Each hop was visible in event data; none of
them required malware reverse engineering to explain.
**Outcome:** documented containment sequence, persistence locations to check, and the specific event
IDs an analyst should query next time.

## Report 4 — NIDS rule analysis

**Scope:** Snort and Zeek output from a lab network under active scanning and tunnelling.
**Method:** compared alerts against expected traffic, separated true positives from noisy rules, then
wrote and tested adjustments.
**Finding:** the highest-volume alerts were port scans — individually low severity, but useful as an
early signal when followed by service-specific probes. DNS tunnelling was visible only when the rule
considered query length and frequency, not just the domain.
**Outcome:** a set of rule changes with the false-positive trade-off of each one written down.

## Report 5 — Linux privilege escalation

**Scope:** a boot2root Linux machine, approached from the attacker side.
**Method:** service enumeration, then version-to-vulnerability reasoning, then local enumeration for
misconfigurations after the initial foothold.
**Finding:** the box was vulnerable through two independent paths — an outdated network service and a
SUID binary that trusted its environment. Either alone would have been enough.
**Outcome:** a red-team write-up that ends with remediation for both paths, written for a system
administrator rather than for a CTF scoreboard.

## Report 6 — Windows SMB exploitation

**Scope:** a boot2root Windows machine with an unpatched SMB service.
**Method:** service identification, vulnerability confirmation against the advertised version, then
post-exploitation credential handling.
**Finding:** the host was missing a critical SMB patch on an end-of-life platform, and credential
material recovered after exploitation was weak enough to crack offline.
**Outcome:** a write-up that treats the patch as a stop-gap and argues the real fix is retiring the
platform, plus SMB hardening guidance.

---

## Automation — Python tooling

Three small utilities, written because the documentation work was repetitive:

| Script | What it does | Why it exists |
| :--- | :--- | :--- |
| `create_writeup.py` | Scaffolds a report directory with a pre-filled template for blue-team or red-team write-ups | Keeps report structure identical across cases |
| `generate_master_study_plan.py` | Builds a formatted study-plan workbook and document from a module list | Removes manual table formatting from planning |
| `generate_syllabus_doc.py` | Generates a structured syllabus document with consistent styling | Same reason, for the curriculum document |

They are small, unglamorous scripts. They are included because they show the habit: if a task will be
repeated more than twice, automate the boring part and spend the time on the analysis.

## Home lab

A local SOC lab was built during the SIEM module: a Splunk instance ingesting host and network logs
from lab machines, with searches and a dashboard built on top. The lab is where the log-analysis
notes in [Study Notes](../05-study-notes/README.md) were tested before being written down.

## Python tools

- [zeek_conn_summary.py](python-tools/zeek_conn_summary.py) - summarises a Zeek `conn.log`: talkers, byte counts, odd ports, long connections, large transfers. Usage and sample output in [python-tools/README.md](python-tools/README.md).
