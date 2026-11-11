# 04 — SOC Operations and Phishing

_Notes from the SOC modules and the phishing analysis work._

## Triage is a decision, not a reading exercise

Every alert ends in exactly one of three states:

1. **True positive** — the activity is real and unwanted. Write the verdict, state the impact, recommend
   the action.
2. **False positive** — the activity is real but expected. Write why, and propose the tuning so the
   same alert does not cost the next analyst the same twenty minutes.
3. **Cannot decide yet** — legitimate, and must be written down with the specific next step and owner.
   Silence is not a fourth state.

The failure mode I see in my own early notes: reading until the alert feels understood, then closing it
without a decision. A decision with reasoning beats a confident guess.

## Scope before verdict

A single blocked download is a closed ticket. Three hosts with the same parent process is an incident.
The difference is usually one query — "where else does this appear?" — asked *before* the verdict is
written, not after.

Order I try to follow:

1. What fired, and what was it looking for?
2. What is the smallest piece of evidence that confirms or refutes it?
3. Where else would that evidence appear?
4. Only then: verdict.

## Close-out notes are the product

A note should let a stranger reach the same conclusion without redoing the work. That means:

- the query or source used,
- the specific rows that mattered,
- what was ruled out and how,
- what remains unknown.

Two lines of "investigated, benign" is not a note; it is a promise that nobody will ever review this
alert again.

## Phishing analysis

**Headers first, content second.** Most cases are decided by the sending infrastructure before the body
is read.

| Question | Where the answer is |
| :--- | :--- |
| Did authentication pass for the sending domain? | SPF / DKIM / DMARC results in the header |
| Does the display name match the envelope sender? | `From` versus `Return-Path` / `Received` chain |
| Which host actually handed the message over? | The `Received` chain, read bottom-up |
| Where does the link really go? | The URL, not the anchor text |
| Did anyone click, and did anything run? | Mail gateway verdict, proxy log, endpoint telemetry |

**Look for the mismatch, not the ugliness.** Poor design is not evidence. A display name that disagrees
with the envelope sender is.

## The user-facing question decides containment

Before judging how convincing a lure was, answer: did the user open it, and did anything execute? That
answer — not the quality of the email — determines whether this is a five-minute ticket or a
containment.

## What I would do differently

- Ask "where else" earlier. I have caught myself writing a verdict before scoping twice.
- Keep a running indicator table across cases; the same infrastructure reappears more often than
  expected.
