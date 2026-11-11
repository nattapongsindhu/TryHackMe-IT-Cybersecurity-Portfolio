# 3. Skills Learned

Each row pairs a skill with the work that proves it. If a row has no evidence link, it is a skill I
practised inside a room but have not yet written up — stated honestly rather than padded.

| Skill | What I can do | Evidence |
| :--- | :--- | :--- |
| **Networking** | Read PCAPs and explain a conversation end to end: TCP handshake, HTTP request/response, DNS lookups, TLS setup. Spot beaconing and tunnelling by timing and volume, not by payload alone. | [Report 1 — Wireshark traffic analysis](06-practical-evidence/README.md#report-1--network-traffic-analysis) |
| **Linux** | Navigate a filesystem, manage permissions, read auth and system logs, inspect running processes, and explain what a suspicious `sudo`, cron entry or SUID binary looks like from the defender side. | [Report 5 — Linux privilege escalation](06-practical-evidence/README.md#report-5--linux-privilege-escalation) |
| **Cybersecurity fundamentals** | Apply the Pyramid of Pain, Cyber Kill Chain and MITRE ATT&CK to label an intrusion consistently, and explain why an indicator is cheap or expensive for an attacker to change. | [03 — MITRE mapping in study notes](05-study-notes/README.md#mitre-attck-in-practice) |
| **SOC operations** | Work an alert queue: triage, gather evidence, decide true/false positive, write the close-out note, escalate when the scope is bigger than the ticket. | [Report 2 — SIEM investigation](06-practical-evidence/README.md#report-2--siem-alert-investigation) |
| **Log analysis** | Read Windows event logs, Sysmon telemetry, web server logs and Splunk searches; correlate a process tree with network activity to reconstruct an event. | [Report 3 — Windows event log investigation](06-practical-evidence/README.md#report-3--windows-endpoint-investigation) |
| **Incident response** | Follow a containment-first sequence on a compromised host: scope, isolate, collect, eradicate, recover, document. | [Report 3](06-practical-evidence/README.md#report-3--windows-endpoint-investigation) |
| **Detection engineering** | Write and test NIDS rules, then explain the false-positive trade-off of each rule. | [Report 4 — NIDS alert analysis](06-practical-evidence/README.md#report-4--nids-rule-analysis) |
| **Phishing analysis** | Inspect headers, URLs and attachments; separate a suspicious-but-legitimate mail from a real lure. | [Study notes — phishing](05-study-notes/README.md#phishing-analysis) |
| **Documentation** | Produce a report a manager can read without the terminal: scope, evidence, verdict, impact, fix. | All six write-ups |
| **Python** | Write small utilities that remove repetitive work (report scaffolding, document generation). | [Automation](06-practical-evidence/README.md#automation--python-tooling) |

## The three skills I would lead with in an interview

1. **Log analysis under uncertainty.** Most alerts do not arrive with a verdict attached. Being able
   to say "here is what the evidence supports, here is what it does not" is the job.
2. **Writing.** A finding that is not written down is not a finding. Every investigation here ends
   with a short report that states scope, evidence, verdict and recommended action.
3. **Careful scoping.** Before touching a host, establish what else might be affected — the difference
   between closing a ticket and missing a campaign.
