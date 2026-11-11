# 8. Lessons Learned

What this sprint changed in how I work — written as statements I could defend in an interview, not as
a list of topics covered.

## 1. The alert is a question, not an answer

My first instinct used to be "is this malicious?". The more useful question is "what decision does
this alert need, and what evidence would change my mind?". That reframing cut my triage time and made
close-out notes shorter and more useful.

## 2. Scope is the difference between a ticket and an incident

A single suspicious process is a ticket. The same process on three hosts, started by the same parent,
is an incident. Asking "where else would this appear?" before writing a verdict is now a habit, and it
is usually one query.

## 3. Evidence has a half-life

Volatile state disappears the moment you reboot or clean. I now capture process lists, network
connections and scheduled tasks before touching anything, because the alternative is explaining an
incident I can no longer prove.

## 4. Writing is part of the investigation, not paperwork afterwards

The write-up is where inconsistencies surface. Twice I found a gap in my own reasoning only while
writing the timeline. If the report cannot state the finding in one sentence, the analysis is not
finished.

## 5. Frameworks are for consistency, not for decoration

Mapping to MITRE ATT&CK is useful because it forces precision: which technique, on which evidence. It
is not useful as a list of impressive-sounding IDs. A short, defensible mapping beats a long one.

## 6. Knowing the attacker's side made me a better defender

The two boot2root machines were the most uncomfortable part of the sprint and the most instructive.
Seeing how quickly a misconfigured SUID binary or an unpatched SMB service turns into full control
changed how I prioritise findings: I now rank by "what does this give an attacker next", not by CVSS
alone.

## 7. Consistency is a security property of documentation

Six reports with the same structure are worth more than six brilliant reports with six different
structures, because a reviewer can compare them. This is also why the reports were generated from a
template rather than from a blank page each time.

## What I would do differently

- **Start the write-up on day one of an investigation**, not after the verdict.
- **Keep a running indicator table** across cases; the same infrastructure reappears more often than
  expected.
- **Time-box the enumeration phase.** On the red-team boxes I over-enumerated before acting, which
  cost time without changing the outcome.
