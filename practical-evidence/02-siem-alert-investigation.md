# 02 — SIEM Alert Investigation

| Field | Detail |
| :--- | :--- |
| Type | Alert triage (blue team) |
| Tools | Splunk, SPL (`stats`, `eval`, `table`, `where`) |
| Data | Roughly 12,000 events from a simulated incident |
| Outcome | True positive — impersonated account leading to a C2 stager |

## Scope

A Splunk dataset for a simulated intrusion, with an alert that pointed at unusual account activity. The
job was to triage it to a verdict and write a close-out note.

## Method

1. **Narrow first** — index and time window around the alert, so the search returns the incident rather
   than the month.
2. **Build a timeline** — authentication events, process activity and network connections in one view,
   ordered by time.
3. **Correlate** — the suspicious account activity checked against the authentication record to see
   whether the account was used by a human or by something automated.
4. **Test the alternative** — the benign explanation (an administrator working late) checked explicitly
   rather than assumed away.

## Finding

The alert looked benign because of the account name: a **homoglyph display name** was used to imitate a
legitimate account, so the activity read as "the usual admin" at first glance. Once the events were
lined up by time, the pattern was a stager execution followed by outbound command-and-control traffic.

Two things decided the case: the account naming trick, and the fact that the stager's process did not
appear in the logon record as a normal user session.

## What this demonstrates

- Correlating identity, process and network views instead of reading one index.
- Treating a familiar-looking account name as a hypothesis to test, not a fact.
- Writing a verdict that names the evidence, not just the conclusion.

## Limits

The dataset is a simulation with a bounded time window. Real environments have weeks of background noise
around the same event, which changes the cost of the "widen the window" step significantly.

## Detection I would add

The stager produced a process-and-network pair that was visible in the data before the alert fired. A
rule keyed on that pairing (unusual parent, outbound connection shortly after) would have surfaced the
case earlier than the account-based alert did.
