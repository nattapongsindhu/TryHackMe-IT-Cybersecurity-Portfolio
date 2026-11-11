# Zeek conn.log Summariser

A small command-line tool built while working through network traffic analysis. Standard library only —
no dependencies, one file — because the first minutes of an investigation should not need a
`pip install`.

| Tool | What it does |
| :--- | :--- |
| [`zeek_conn_summary.py`](zeek_conn_summary.py) | Summarises a Zeek `conn.log`: talkers, byte counts, odd ports, long connections, large transfers |

**All sample data in this folder is synthetic.** `sample_conn.log` was written by hand to exercise the
tool; its addresses come from the IETF documentation ranges (`192.0.2.0/24`, `198.51.100.0/24`,
`203.0.113.0/24`) and a private lab range (`10.10.5.0/24`). No capture from a real network is included.

## zeek_conn_summary.py

### Usage

```bash
python zeek_conn_summary.py sample_conn.log
python zeek_conn_summary.py conn.log --top 5
python zeek_conn_summary.py conn.log --json
```

### What it prints

| Section | Meaning |
| :--- | :--- |
| [1] Volume | Connection count, unique sources and destinations, connection-state mix |
| [2] Talkers | Sources ranked by number of connections |
| [3] Senders | Sources ranked by bytes sent — different question, different answer |
| [4] Destinations | Where the traffic went |
| [5] Uncommon low ports | Anything below 1024 that is not DNS, HTTP, NTP or HTTPS |
| [6] Longest connections | Duration outliers; sessions that stay open are worth a look |
| [7] Largest transfers | Volume outliers; the pair that moved the most bytes |

### Sample output

```text
====================================================================
 ZEEK conn.log TRIAGE   10 connections
====================================================================

[1] VOLUME
    connections        : 10
    unique sources     : 3
    unique destinations: 5
    connection states  : SF=8, REJ=1, S0=1

[2] TOP 5 TALKERS (by connections)
        4  ########################  10.10.5.21
        3  ##################        10.10.5.44
        3  ##################        10.10.5.55

[3] TOP 5 SENDERS (by bytes)
       10.4 KB  10.10.5.44
        3.5 KB  10.10.5.21
         828 B  10.10.5.55

[4] TOP 5 DESTINATIONS
        4  45.155.205.233
        2  93.184.216.34
        2  185.199.108.153
        1  10.10.5.10
        1  8.8.8.8

[5] UNCOMMON LOW PORTS (not 53/80/123/443)
        1  port 445
        1  port 22

[6] LONGEST CONNECTIONS
        31.0s  10.10.5.21      -> 45.155.205.233:22      -        sent 2.0 KB
        12.5s  10.10.5.44      -> 45.155.205.233:3389    -        sent 8.2 KB
```

### How I use the output

1. **Start at [5].** Internal hosts talking to odd low ports is rarely routine.
2. **Then [7].** A host that moved more than everyone else is either doing backups or doing something new.
3. **Then [2] and [3] together.** The loudest host and the biggest sender are often different machines; that
   difference is interesting.
4. **Only then** open the raw log and read the rows for the host of interest.

### What it does not do

- It does not resolve names, geolocate addresses, or score reputation. Those need external data.
- It does not read PCAP. It reads Zeek's TSV `conn.log` only.
- It does not judge. Every section is a pointer to rows worth reading.

## Sample data

`sample_conn.log` is synthetic: three internal clients, one web server, one DNS server, and one external
address that receives an SSH, an RDP and an SMB attempt. No real network data is included.
