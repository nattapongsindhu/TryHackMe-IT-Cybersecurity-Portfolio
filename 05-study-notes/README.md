# 5. Study Notes

Concept summaries written in my own words. These are **my notes, not walkthroughs**: no flags, no
room answers, and no step-by-step solutions for rooms that are still active on TryHackMe.

The point of each section is to explain the idea well enough that I could defend it in an interview
or apply it to a ticket I have never seen.

## Networking

- **Everything is a conversation.** Most investigations are decided by who started a conversation,
  with whom, how long it lasted, and how much was said — not by the payload.
- **TCP gives you a story with a beginning and an end.** Handshake, data, teardown. A connection that
  never completes the handshake tells you about reachability; one that completes and then idles tells
  you about a client that is waiting for instructions.
- **DNS is the quiet channel.** Name resolution happens before almost everything else, which is why
  it is both a useful control point and a favourite exfiltration path. Volume and entropy of queried
  names matter more than the names themselves.
- **Segmentation is a detection strategy, not only a prevention one.** If a workstation can reach a
  domain controller directly, you have removed one of the cheapest signals you had.

## Linux

- **Permissions are the attack surface.** SUID binaries, writable service files, permissive sudo
  entries and cron jobs are the four places to look first when asking "how would someone go from a
  user shell to root here".
- **Logs are spread across the system on purpose.** Authentication, kernel, service and application
  events land in different places; a single suspicious login usually has evidence in two of them.
- **Read-only first.** Before changing anything on a suspected host, record what is running, what is
  listening, and what is scheduled — that evidence disappears the moment you restart a service.

## Security fundamentals

- **Prevention fails eventually; detection is what buys time.** A control that blocks 99% of attempts
  still leaves the question of what happened in the 1%.
- **Indicators have a shelf life.** A hash dies when the file is rebuilt; an IP dies when the
  infrastructure moves; behaviour survives. This is the whole point of the Pyramid of Pain.
- **Least privilege is the cheapest containment.** The blast radius of a compromised account is
  decided long before the compromise.

## SOC operations

- **Triage is a decision, not a reading exercise.** Every alert ends in one of: true positive,
  false positive, or "cannot decide yet — here is what I need". The third answer is legitimate and
  must be written down with the next step.
- **Scope before verdict.** A single blocked download is a closed ticket; three hosts with the same
  parent process is an incident. The difference is one query.
- **Close-out notes are the product.** A future analyst — or an auditor — should be able to read the
  note and reach the same conclusion without repeating the work.

## Log analysis

- **Start from the alert, not the log.** Know which detection fired and what it was looking for;
  otherwise you will spend an hour reading healthy traffic.
- **Build a timeline before an opinion.** Order the evidence by time, then look for the gaps — missing
  events are often more informative than present ones.
- **Correlate two sources minimum.** A process name alone means nothing; the same process starting
  from an unusual parent and opening an outbound connection means something.
- **Windows event IDs worth memorising first:** 4624 (logon), 4625 (failed logon), 4688 (process
  creation), 7045 (service installed). With Sysmon, process creation and network connection events
  give you the same story with more detail.

## Incident response

- **Contain, then investigate.** Every extra minute of dwell time is another host to clean.
- **Preserve before you clean.** A memory image and the volatile state matter more than a tidy
  desktop; eradication without evidence produces an incident you cannot explain later.
- **Write the timeline while it is fresh.** Human memory of an incident degrades faster than the logs.
- **Post-incident is where the value is.** The report should change at least one control, one
  detection, or one process — otherwise the same incident is scheduled to happen again.

## MITRE ATT&CK in practice

- **Map to the technique that describes what you saw, not the one that sounds worst.** A PowerShell
  download is a download technique until you can show what it executed.
- **Tactics are the story, techniques are the evidence.** "Discovery" tells a manager where in the
  attack you caught it; the technique ID tells an engineer what to detect.
- **A mapping is a claim.** If the evidence only supports "execution via scripting interpreter", say
  that, and leave the follow-on techniques out.

## Phishing analysis

- **Headers first, content second.** Authentication results and the sending infrastructure decide most
  cases before you read the body.
- **Look for the mismatch, not the ugliness.** Poor design is not evidence; a display name that
  disagrees with the envelope sender is.
- **Decide the user-facing question early:** did anyone click, and did anything run? Containment
  depends on that answer, not on how convincing the lure was.
