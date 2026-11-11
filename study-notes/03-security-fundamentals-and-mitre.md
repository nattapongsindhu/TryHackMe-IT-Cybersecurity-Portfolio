# 03 — Security Fundamentals and MITRE ATT&CK

_Notes on the frameworks that keep findings comparable across cases._

## Prevention fails eventually; detection buys time

A control that blocks 99% of attempts still leaves the question of what happened in the 1%. This is not
a pessimistic view, it is the reason a SOC exists. Every detection decision I make now starts from:
"if this got through, what would I see?"

## Indicators have a shelf life

This is the Pyramid of Pain in one sentence.

| Indicator | Attacker cost to change | Detection value |
| :--- | :--- | :--- |
| File hash | Rebuild the binary | Low — dies on first recompile |
| IP address | Move infrastructure | Low to medium |
| Domain | Register another | Medium |
| Host artefact (registry key, service name) | Change the build | Medium to high |
| Tool / malware family behaviour | Re-engineer | High |
| TTP | Change how they work | Highest |

A detection written only on hashes is a detection that expires silently. The higher up the pyramid you
write, the longer the rule lives — and the more careful you have to be about false positives.

## Tactics are the story, techniques are the evidence

- **Tactic** = where in the attack you are ("Discovery", "Persistence"). Useful for a manager, useful
  for a report narrative.
- **Technique** = what was actually observed (T1059, T1547…). Useful for an engineer, useful for
  building a detection.

A mapping is a claim. If the evidence only supports "execution via scripting interpreter", write that
and stop. Adding the next three techniques because they usually follow is how a report stops being
evidence.

## Kill chain versus ATT&CK

| Framework | Shape | Best used for |
| :--- | :--- | :--- |
| Cyber Kill Chain | Seven linear stages | Telling the story of one intrusion, start to finish |
| MITRE ATT&CK | Matrix of tactics and techniques | Labelling evidence precisely and comparing across cases |
| Unified Kill Chain | 18 integrated stages | Reasoning about modern intrusions that skip stages |

They are not competing. The kill chain is a narrative tool; ATT&CK is a labelling vocabulary. Using
both is not redundant — one explains, the other indexes.

## What I actually do in a report

1. Write the timeline first, with no labels.
2. Label each entry with the technique the evidence supports.
3. Group the labels by tactic and check nothing is claimed without an entry behind it.
4. Delete any label that only exists because "that is usually what happens next".

## Still thin

Detection-rule authoring at TTP level (Sigma) is on the next-steps list. I can map evidence to
techniques reliably; turning that into durable rules is the next skill.
