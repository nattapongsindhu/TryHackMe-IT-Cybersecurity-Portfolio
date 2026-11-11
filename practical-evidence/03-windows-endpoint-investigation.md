# 03 — Windows Endpoint Investigation

| Field | Detail |
| :--- | :--- |
| Type | Endpoint investigation / DFIR (blue team) |
| Tools | Windows Event Viewer, Sysmon, process lineage |
| Data | A compromised Windows host from a DFIR lab |
| Outcome | Full chain reconstructed; containment sequence and persistence checklist produced |

## Scope

A Windows host compromised through a document-based exploit chain. The question was not "is it
infected" but "what happened, in what order, and what would bring it back after a reboot".

## Method

1. **Process creation first** — parent/child relationships; the anomaly is usually in the parent, not
   the child.
2. **Persistence second** — services, scheduled tasks, run keys, WMI subscriptions.
3. **Network third** — which of those processes opened outbound connections, to where.
4. **Timeline last** — everything in order, so the report argues rather than lists.

## Finding

The chain moved through four steps:

1. a document handler spawned a scripting interpreter,
2. the interpreter launched a tunnelling binary,
3. that binary established the remote channel,
4. a privilege-escalation step followed on the same host.

Every one of those steps was visible in event data. None of them required malware reverse engineering to
explain — which is the part worth saying out loud, because "we need a reverse engineer" is often used to
delay a decision that the logs already support.

## What this demonstrates

- Reading a Windows host as a sequence of parent/child relationships rather than a list of alerts.
- Distinguishing the infection vector from the persistence mechanism.
- Producing a containment sequence someone else could follow.

## Limits

The host was a lab image with clean telemetry. On a real endpoint, half the value would come from
comparing against a known-good baseline, which the lab does not provide.

## Containment sequence produced

1. Isolate the host network-side (do not power it off — memory and volatile state).
2. Capture process list, network connections and scheduled tasks before any cleanup.
3. Remove persistence in the order: services, tasks, run keys, WMI.
4. Reset credentials for any account that authenticated from the host.
5. Reimage rather than clean if the root cause is not identified.

> Note: in this lab the isolation action was a recommendation in the report, not an executed step — the
> environment did not provide endpoint isolation controls. Stated here rather than implied.
