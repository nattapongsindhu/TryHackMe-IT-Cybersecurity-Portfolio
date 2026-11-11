# 04 — NIDS Rule Analysis

| Field | Detail |
| :--- | :--- |
| Type | Detection engineering (blue team) |
| Tools | Snort, Zeek |
| Data | Lab network under scanning and tunnelling activity |
| Outcome | Rule changes with the false-positive trade-off of each documented |

## Scope

Snort and Zeek output from a lab network, with the task of deciding which alerts were worth keeping and
writing adjustments for the rest.

## Method

1. **Baseline the noise** — what fires constantly and why.
2. **Compare against expected traffic** — which alerts correspond to activity that the network is
   supposed to do.
3. **Adjust, then re-run** — change one thing at a time so the effect is attributable.
4. **Write down the trade-off** — every rule change moves false positives in one direction and blind
   spots in the other.

## Finding

Three things stood out:

- **Port scans dominate volume and are individually low value.** Their worth is contextual: a scan
  followed by service-specific probes tells a different story than a scan that goes nowhere.
- **DNS tunnelling is invisible to naive rules.** It looks like a resolver doing a lot of work. Query
  length and frequency carry the signal; the domain name alone does not.
- **Most of the improvement came from removing rules, not adding them.** Two noisy rules were consuming
  analyst attention without ever producing a real finding.

## What this demonstrates

- Thinking about an alert as a cost per true finding, not as a success.
- Writing a rule with its false-positive case stated in advance.
- Understanding that tuning is subtractive before it is additive.

## Limits

Lab traffic is representative, not real. The false-positive rates measured here would not transfer to a
production network without re-baselining — which is the same caveat any detection engineer would give.

## Example of the trade-off

A rule that alerts on long DNS queries catches tunnelling, and also catches a service that resolves
long tracking hostnames. Narrowing the rule by frequency fixes the false positive but means a slow
tunnel (one query every five minutes) is missed. The choice depends on what the network actually does —
which is why the baseline step comes first.
