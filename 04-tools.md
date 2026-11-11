# 4. Tools & Technologies

Tools I have actually used in labs and investigations — not a list of things I have read about.

## Network analysis

| Tool | Used for | Where |
| :--- | :--- | :--- |
| **Wireshark** | Packet capture review, display filters, following TCP streams, extracting transferred files | Report 1, network monitoring module |
| **tcpdump** | Command-line capture and quick filtering on a Linux host | Network traffic analysis module |
| **TShark** | Packet analysis from the terminal when a GUI is not available | Wireshark module |
| **Nmap** | Host discovery, port and service enumeration during red-team machines | Reports 5 and 6 |
| **Snort** | Writing and testing NIDS rules against scan and exploit traffic | Report 4 |
| **Zeek** | Protocol-aware network logs; reading `conn`, `dns`, `http` output | Report 4 |

## Endpoint and log analysis

| Tool | Used for | Where |
| :--- | :--- | :--- |
| **Splunk (SPL)** | Searching and correlating events; `stats`, `eval`, `table`, `where`; building a dashboard | Report 2 |
| **Windows Event Viewer** | Reading security, system and application logs; event IDs 4624/4625/4688/7045 | Report 3 |
| **Sysmon** | Process creation, network connection and file telemetry | Report 3 |
| **Sysinternals** (Procmon, Autoruns, Process Explorer) | Process and persistence inspection on Windows | Windows monitoring module |
| **Volatility** | Memory forensics — recovering process and artifact data from a RAM image | DFIR module |
| **Autopsy** | Disk and file-system forensics, timeline review | DFIR module |

## Systems and scripting

| Tool | Used for | Where |
| :--- | :--- | :--- |
| **Linux CLI** | File system, permissions, process and log inspection, package management | Throughout |
| **Bash** | Chaining commands during triage and enumeration | Throughout |
| **Python 3** | Three small utilities: report scaffolding, study-plan generation, syllabus document generation | [Automation](06-practical-evidence/README.md#automation--python-tooling) |
| **Git / GitHub** | Version control, Markdown documentation, this repository | Portfolio |

## Frameworks and references

| Framework | How I use it |
| :--- | :--- |
| **MITRE ATT&CK** | Labelling each step of an intrusion with a tactic and technique so findings are comparable across cases |
| **Cyber Kill Chain** | Structuring the narrative of an attack from recon to objective |
| **Pyramid of Pain** | Deciding which indicators are worth writing a detection for |
| **NIST SP 800-61 (concepts)** | Incident lifecycle: preparation, detection and analysis, containment/eradication/recovery, post-incident |

> Tools change; the reasoning does not. The notes in [Study Notes](05-study-notes/README.md) are
> written around the reasoning, with the tools named only as the instrument used that day.
