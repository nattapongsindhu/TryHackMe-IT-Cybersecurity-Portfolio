# Security Check — Pre-Publish Review

This repository is public. Before publishing, it was reviewed against the list below. The check is
documented so a reader can see the standard, and so future updates keep the same bar.

## Checklist

| # | Item | Rule applied | Result |
| :---: | :--- | :--- | :---: |
| 1 | API keys and tokens | No `api_key`, `apikey`, `token`, `secret`, `bearer`, `ghp_`, `AKIA` values | Pass |
| 2 | Passwords and credentials | No `password=`, no credential dumps, no captured hashes from labs | Pass |
| 3 | TryHackMe flags | No `THM{...}` strings, no flag screenshots | Pass |
| 4 | Room answers | No question-and-answer pairs from rooms that are still active | Pass |
| 5 | Active-room walkthroughs | No step-by-step exploitation of rooms still available to other learners | Pass |
| 6 | Personal data | Only the portfolio owner's name (already printed on the certificates). No address, phone, student ID or employer detail | Pass |
| 7 | Private lab data | No internal hostnames, IP ranges or configuration from any employer or private environment | Pass |
| 8 | Screenshots | No screenshots from active labs; only the two issued certificates | Pass |
| 9 | Sample data | `sample_access.log` and `sample_conn.log` are synthetic; every address is a documentation range or a private lab range | Pass |

## How the check is run

```powershell
# run from the repository root
Get-ChildItem -Recurse -File -Include *.md,*.py,*.log,*.json,*.yml,*.yaml |
  Select-String -Pattern 'THM\{','api[_-]?key','password\s*=','secret','ghp_','AKIA','BEGIN .*PRIVATE KEY'
```

Any hit is reviewed by hand before publication. A hit is not automatically a failure — this file itself
contains the patterns it searches for — but every hit must be explained.

## IP ranges used in examples

The synthetic log and the evidence summaries use the IETF documentation ranges, which cannot route on
the public internet:

| Range | Purpose |
| :--- | :--- |
| `192.0.2.0/24` | TEST-NET-1 |
| `198.51.100.0/24` | TEST-NET-2 |
| `203.0.113.0/24` | TEST-NET-3 |
| `10.10.14.0/24` | Private lab range, web access log sample |
| `10.10.5.0/24` | Private lab range, Zeek conn.log sample |

## What is deliberately not here

- **Full investigation reports.** They contain room answers and flags from labs that are still active.
  They stay in a private working repository; this repository carries the sanitised summary.
- **Capture files and sample malware.** Not publishable, and not necessary to demonstrate the method.
- **Screenshots of terminals.** They leak room identifiers and, sometimes, answers.

## Reporting a problem

If you believe something here exposes a secret, a flag, or personal data, open an issue or contact me
through the links on the [Certificates page](certificates/README.md). I will remove it first and
investigate afterwards.
