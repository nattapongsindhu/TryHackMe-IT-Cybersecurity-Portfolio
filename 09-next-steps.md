# 9. Next Steps

The sprint answered "can I learn this". The next question is "can I do it under production
conditions". This is the 90-day plan that follows, and how each item will be evidenced.

## 90-day plan

| Priority | Focus | What I will build | How it will show up here |
| :---: | :--- | :--- | :--- |
| 1 | **Linux depth** | Log sources, systemd units, permissions and hardening on a self-built Linux host; a written hardening checklist | New study note + a lab write-up |
| 2 | **Python for security work** | A real log parser (auth logs and web logs) that outputs a timeline and flags anomalies, replacing the current three scaffolding scripts | A tool page with sample output |
| 3 | **Network security** | A segmented home lab with a firewall, IDS and a deliberately vulnerable target; detect, then explain each alert | Lab report with detection reasoning |
| 4 | **SIEM** | Reproduce the Splunk lab with a second stack (Elastic or Wazuh) to prove the concepts are not tool-specific | Comparison note: same detection, two platforms |
| 5 | **CompTIA Security+** | Study and sit the exam | Certificate added to this repository |

## Beyond 90 days

| Horizon | Goal |
| :--- | :--- |
| 6 months | Detection engineering as a practice: a small rule pack with documented false-positive tuning |
| 12 months | Threat hunting: hypothesis-driven hunts written up as reports, not as dashboards |
| Ongoing | One incident-style investigation per month, published as a sanitised summary |

## What "done" looks like

Not a certificate count. The measure I am using:

- I can take an alert I have never seen and reach a defensible verdict without asking for help.
- Every claim I make about a host is backed by a query I can re-run.
- A report I wrote six months ago still makes sense to a stranger.

## Why this is public

Recruiters and SOC leads can see the trajectory, not only the current state. If the plan changes —
and it will — this page gets updated rather than quietly deleted.
