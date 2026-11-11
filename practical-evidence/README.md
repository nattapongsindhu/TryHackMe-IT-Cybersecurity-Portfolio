# Practical Evidence

Work produced during the sprint. Each item is an **evidence summary**: what the case was, what I did,
what the result was, and what I could not verify.

| # | Evidence | Type | Result |
| :---: | :--- | :--- | :--- |
| 01 | [Network traffic analysis](01-network-traffic-analysis.md) | Packet capture lab | Multi-stage exchange reconstructed from a PCAP |
| 02 | [SIEM alert investigation](02-siem-alert-investigation.md) | Alert triage | True positive: impersonated account to C2 stager |
| 03 | [Windows endpoint investigation](03-windows-endpoint-investigation.md) | Endpoint / DFIR | Full chain from document handler to privilege escalation |
| 04 | [NIDS rule analysis](04-nids-rule-analysis.md) | Detection engineering | Rule changes with the false-positive trade-off written down |
| 05 | [Linux privilege escalation](05-linux-privilege-escalation.md) | Red team | Two independent paths to root, both with remediation |
| 06 | [Windows SMB exploitation](06-windows-smb-exploitation.md) | Red team | Unpatched SMB on an end-of-life host, weak credentials |
| 07 | [Python log analyzer](python-log-analyzer/) | Tool I built | Parses access logs, flags scanners and injection payloads |
| 08 | [Zeek conn.log summariser](zeek-conn-summary/) | Tool I built | Top talkers, long connections, large transfers, uncommon ports |

The long-form reports live in a **private working repository**. They contain room answers and flags for
labs that are still active, so they are deliberately not published. If you are reviewing an application
and want the detailed version, ask and I will send it.

## What each summary contains

- **Scope** — what the case covered and where the data came from.
- **Method** — the order of the work, which is usually the transferable part.
- **Finding** — what the evidence supported, stated at the level the evidence allows.
- **Result and limits** — the verdict or outcome, plus what could not be confirmed.

## Note on realism

These are lab and platform cases, not production incidents. Where a lab could not provide something —
endpoint isolation, for example — the summary says so instead of describing an action I did not take.
