# 01 — Networking and Traffic

_Concepts behind packet analysis, written after the Wireshark investigations._

## Everything is a conversation

Most investigations are decided by four facts: who started the conversation, with whom, how long it
lasted, and how much was said. Not by the payload. A payload can be encrypted; the shape of the
conversation usually cannot be hidden.

## TCP tells you a story with a beginning and an end

- Handshake → data → teardown. You can place every packet on that map.
- A connection that never completes the handshake is a statement about reachability, not about content.
- A connection that completes and then sits idle is a client waiting for instructions. That pattern —
  regular small outbound connections at fixed intervals — is what beaconing looks like in a capture.

## DNS is the quiet channel

Name resolution happens before almost everything else, which makes it both a useful control point and a
convenient exfiltration path.

- Volume matters more than content: a workstation that resolves 400 unique names per hour at 02:00 is
  interesting regardless of the names.
- Entropy matters too: long, random-looking subdomains under one parent domain are a signature of
  tunnelling.
- Blocking a resolver is a blunt control; monitoring it is a detection.

## Ports and services are context, not evidence

"Port 445 is open" is not a finding. "Port 445 is open on a host that should not be running SMB, and a
session was established from an unrelated subnet" is a finding. The port supplies the context; the
session supplies the evidence.

## Segmentation is a detection strategy

If a workstation can reach a domain controller directly, you have removed one of the cheapest signals
you had: the alert that fires when something crosses a boundary it should not cross. Segmentation is
usually discussed as prevention; it earns its keep as detection.

## What a packet capture cannot tell you

- Why the user did it.
- Whether the payload actually executed after download.
- What happened on the host outside the network path.

Those questions need endpoint telemetry. Knowing where the capture stops is as important as reading it.

## Reading strategy I now use

1. Protocol hierarchy first — what kinds of traffic exist at all.
2. Conversations next — who talked to whom, how much.
3. Then streams — but only for the conversations that carried data.
4. Then the timeline — because ordering is where the argument is made.

## Still thin

TLS inspection and decryption are areas where I can read the concept but have not done the work.
Noted rather than hidden.
