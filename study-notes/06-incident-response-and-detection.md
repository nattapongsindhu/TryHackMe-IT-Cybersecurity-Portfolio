# 06 — Incident Response and Detection Engineering

_Notes from the DFIR modules and the two containment-focused investigations._

## Contain, then investigate

Every extra minute of dwell time is another host to clean. The order that matters:

1. **Scope** — which hosts, which accounts, which time window.
2. **Contain** — isolate the host network-side; disable the account if it is the vector.
3. **Preserve** — memory image, volatile state, relevant logs, before anything is cleaned.
4. **Eradicate** — remove the persistence, not just the process.
5. **Recover** — restore, then watch for the same behaviour returning.
6. **Report** — timeline, verdict, impact, and the control that would have caught it.

Skipping step 3 is the most common mistake, because step 2 feels urgent and step 3 feels slow. The
cost shows up two weeks later when someone asks for proof.

## Persistence is the part people forget

Removing a malicious process is not eradication. On Windows the usual suspects are:

- a service (event ID 7045 is your friend),
- a scheduled task,
- a run key,
- a WMI subscription.

On Linux: a systemd unit, a cron entry, an `rc.local` line, an SSH key. Each of these survives a reboot
and undoes a "clean" host.

## Detection engineering: a rule is a claim about behaviour

Writing a rule forces precision. "Detect suspicious PowerShell" is not a rule; it is a wish.
"Detect PowerShell spawned by an Office process with an encoded command line" is a rule — and it has a
measurable false-positive rate you can argue about.

Three questions before shipping a rule:

1. **What legitimate activity will this match?** If the answer is "none", the rule is probably too
   narrow to matter.
2. **What will the attacker do next to avoid it?** If the answer is "rename the binary", the rule has a
   short life.
3. **Who will read the alert at 03:00, and what will they do?** A rule nobody can triage is worse than
   no rule.

## NIDS specifics that surprised me

- **Port scans are individually boring and collectively useful.** The value is in the follow-up: a scan
  followed by service-specific probes is a different story from a scan that goes nowhere.
- **DNS tunnelling does not look like an attack.** It looks like a resolver doing a lot of work. Query
  length and frequency carry the signal, not the domain name.
- **Rule tuning is subtractive.** Most of the value came from removing noisy rules, not from adding
  clever ones.

## Reporting

Every investigation here ends with the same structure: scope, evidence, verdict, impact, recommended
action, and a **limits** section. The limits section is the part I am most comfortable defending in an
interview, because it is the part that is honest.

## Still thin

Sigma rule authoring at scale, and detection-as-code pipelines. Both are on the
[next steps](../README.md#9-next-steps) list.
