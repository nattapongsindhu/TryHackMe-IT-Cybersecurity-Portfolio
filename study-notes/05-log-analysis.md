# 05 — Log Analysis

_Notes from the Windows, Linux and web log work behind the investigation summaries._

## Start from the alert, not from the log

Know which detection fired and what it was looking for before opening a query. Otherwise an hour
disappears into healthy traffic that happens to be interesting.

## Build a timeline before forming an opinion

Order the evidence by time, then look for the gaps. Missing events are often more informative than
present ones: a process that should have a parent, a logon with no matching logoff, a download with no
execution.

## Windows event IDs worth memorising first

| Event ID | Meaning | Why it matters |
| :---: | :--- | :--- |
| 4624 | Successful logon | Who got in, from where, with which logon type |
| 4625 | Failed logon | Volume and pattern tell brute force from a typo |
| 4688 | Process creation | The backbone of process-lineage analysis |
| 7045 | Service installed | A favourite persistence mechanism |

Sysmon adds the same story with more detail — process creation with command line and hash, network
connections tied to a process ID, file creation with the initiating process.

## Correlate two sources minimum

A process name alone means nothing. The same process, started by an unusual parent, opening an outbound
connection to an address nobody else talks to, means something. One source is a fact; two sources are
an argument.

## Web logs

- **Status codes tell the story of an attempt.** A wave of 404s from one source is enumeration; a 200
  after a wave of 404s is a successful guess.
- **User agents lie, but they lie consistently.** A scanner advertising itself is easy; the one
  pretending to be a browser is the one worth a rule.
- **The query string is where payloads live.** Decode it before matching, or half the injections look
  like noise — this is exactly the bug I fixed in my own [log analyser](../practical-evidence/python-log-analyzer/README.md).

## A search strategy that works for me

1. **Anchor** — find the one event I am sure about (the alert row).
2. **Widen** — ±10 minutes around it, same host or same account.
3. **Pivot** — take an identifier from that window (process ID, file hash, remote address) and search
   it across the estate.
4. **Bound** — stop when the next pivot returns only what I already know.

## What good looks like

A note that says: "at 14:02 the process `X` was created by `Y`; at 14:03 it connected to `Z`; the same
pattern appears on two other hosts; therefore scope is three hosts." Three sentences, three sources,
one conclusion.
