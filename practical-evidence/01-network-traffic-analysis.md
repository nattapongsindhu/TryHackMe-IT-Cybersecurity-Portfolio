# 01 — Network Traffic Analysis

| Field | Detail |
| :--- | :--- |
| Type | Packet capture lab (blue team) |
| Tools | Wireshark, protocol hierarchy, follow-TCP-stream |
| Data | A provided capture file |
| Outcome | Timeline of a multi-stage exchange, indicators that survive a payload rebuild |

## Scope

A capture provided as part of a traffic-analysis exercise. The task was to work out what happened on
the wire, in order, and to separate the initial contact from the activity that followed.

## Method

1. **Protocol hierarchy** — what kinds of traffic exist at all, and what dominates the capture.
2. **Conversations** — who talked to whom, byte counts, duration; ranked by volume and by novelty.
3. **Stream reconstruction** — only for the conversations that carried data.
4. **Timeline** — every relevant request placed in order, with the host and the protocol noted.

## Finding

The capture showed a staged exchange rather than a single event: an initial request to one host led to a
second download from an unrelated address. The first contact was not the payload — which is the pattern
that makes "the user visited a bad site" an incomplete story.

The useful output was not the file itself but the **behaviour**: what was requested, in what order, and
which infrastructure carried which stage.

## What this demonstrates

- Reading a capture as a sequence rather than as a list of packets.
- Separating "initial access" from "delivery of the thing that matters".
- Choosing indicators that survive the attacker rebuilding the payload — infrastructure and behaviour
  rather than file hashes.

## Limits

The capture ends at the network boundary. Whether the downloaded file executed, and with what
privileges, is not answerable from the PCAP alone — that question needs endpoint telemetry, and the
summary does not pretend otherwise.
