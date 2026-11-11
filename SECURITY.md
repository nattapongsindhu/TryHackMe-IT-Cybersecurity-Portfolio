# 10. Security & Privacy Check

This repository is intended to be public. Before it was published, it was checked against the list
below. The check is documented so a reader can see the standard, and so future updates keep the same
bar.

## What was checked

| # | Item | Rule applied | Result |
| :---: | :--- | :--- | :---: |
| 1 | API keys and tokens | No `api_key`, `apikey`, `token`, `secret`, `bearer`, `ghp_`, `AKIA` strings anywhere | Pass |
| 2 | Passwords and credentials | No `password=`, no credential dumps, no captured hashes from labs | Pass |
| 3 | TryHackMe flags | No `THM{...}` strings, no flag screenshots | Pass |
| 4 | Room answers | No question-and-answer pairs from rooms that are still active | Pass |
| 5 | Walkthroughs of active rooms | No step-by-step exploitation of rooms still available to other learners | Pass |
| 6 | Personal data | Only the portfolio owner's name (it is already on the certificates). No address, phone, student ID or employer detail | Pass |
| 7 | Private lab data | No internal hostnames, IP ranges, or configuration from any employer or private environment | Pass |
| 8 | Screenshots | No screenshots from active labs; only the two issued certificates | Pass |

## How the check is run

```powershell
# run from the repository root
Select-String -Path (Get-ChildItem -Recurse -File -Include *.md,*.py,*.json,*.yml,*.yaml) `
  -Pattern 'THM\{','api[_-]?key','password\s*=','secret','ghp_','AKIA','BEGIN .*PRIVATE KEY'
```

Any hit is reviewed by hand before publication. A hit is not automatically a failure — a sentence like
"no passwords are stored here" will match the pattern — but every hit must be explained.

## What is deliberately not here

- **Full investigation reports.** They contain room answers and flags from labs that are still active.
  They stay in a private working repository; this repository carries the sanitised summary instead.
- **Capture files and sample malware.** Not publishable, and not necessary to demonstrate the method.
- **Screenshots of terminals.** They leak room identifiers and, sometimes, answers.

## Reporting a problem

If you believe something here exposes a secret, a flag, or personal data, please open an issue or
contact me through the profile links on the [Certificates & Links](07-certificates.md) page. I will
remove it first and investigate afterwards.
