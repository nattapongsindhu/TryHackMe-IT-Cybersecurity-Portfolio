# 05 — Linux Privilege Escalation

| Field | Detail |
| :--- | :--- |
| Type | Red team (boot2root machine) |
| Tools | Nmap, Linux command line, local enumeration |
| Outcome | Two independent paths to root, each with remediation |

## Scope

A boot2root Linux machine, approached deliberately from the attacker side. The goal was not the flag —
it was understanding which misconfigurations turn a service foothold into full control.

## Method

1. **Service enumeration** — what is listening, and at which version.
2. **Version-to-vulnerability reasoning** — which of those versions has a known issue, and does the
   behaviour match.
3. **Foothold** — the smallest step that gets a shell.
4. **Local enumeration** — permissions, SUID binaries, scheduled jobs, writable paths.
5. **Escalation** — the path that requires the least luck.

## Finding

The host was vulnerable through two independent paths:

- an **outdated network service** whose version was exploitable, and
- a **SUID binary that trusted its environment**, so its behaviour could be redirected by a normal user.

Either alone would have been enough. That is the finding worth reporting: not "the box was rooted" but
"two separate controls were missing, and fixing one would have left the other".

## What this demonstrates

- Attacker-side reasoning applied to defender priorities: which misconfiguration gives the most for the
  least effort.
- Recognising that a SUID binary is an attack surface, not just a permission bit.
- Writing remediation for a system administrator rather than for a scoreboard.

## Limits

A lab machine built to be vulnerable. The individual techniques are well documented publicly; the value
here is the reasoning order and the remediation, not novelty.

## Remediation produced

1. Patch or retire the outdated service — and note that the distribution was end-of-life, so patching
   is a stop-gap.
2. Remove the SUID bit from the binary, or replace it with something that does not take a path from the
   environment.
3. Re-check for the same pattern on other hosts: SUID binaries whose purpose is convenience rather than
   necessity are usually a fleet-wide habit.
