# Python Log Analyzer

A small web access-log triage tool. Deliberately simple: parse a combined-format log, count sources,
spot scanner user agents, and surface injection-style payloads in the query string.

The point is not that the tool is clever. The point is that triage starts with "what is unusual in this
file", and doing that by hand for the tenth time is a waste of an analyst's hour.

## Files

| File | What it is |
| :--- | :--- |
| `analyze.py` | The analyser — standard library only, no dependencies |
| `sample_access.log` | A synthetic 26-line log covering normal traffic, a scanner, SQL injection, traversal, XSS and a Log4Shell probe |

## Usage

```bash
python3 analyze.py sample_access.log
python3 analyze.py sample_access.log --top 5
```

## What it reports

- request count and unique source IPs
- top source IPs (with a simple bar chart)
- HTTP methods and status-code distribution
- scanner-like user agents (Nikto, sqlmap, nmap, gobuster, curl, python-requests, …)
- injection-style payloads: SQL injection, path traversal, XSS, command injection, Log4Shell
- share of 4xx/5xx responses

## Sample output

```text
File      : sample_access.log
Requests  : 26
Unique IP : 9

Top source IPs
      4  ############################  10.10.14.7
      4  ############################  192.0.2.44
      3  #####################         10.10.14.9
      3  #####################         10.10.14.12
      3  #####################         198.51.100.23

Scanner-like user agents
      4  192.0.2.44        nikto
      3  198.51.100.23     python-requests
      3  203.0.113.61      sqlmap
      3  203.0.113.77      curl/

Injection-style payloads
      3  sql-injection       203.0.113.61
         e.g. /search?q=1%27%20OR%20%271%27=%271
      3  path-traversal      203.0.113.77
         e.g. /../../../../etc/passwd
      2  xss                 192.0.2.90
         e.g. /?q=%3Cscript%3Ealert(1)%3C/script%3E

4xx/5xx responses : 7 (27%)
IPs with scanner UA: 4
```

## The design decision worth explaining

The first version matched payload patterns against the **raw** path, and missed most SQL injection —
the payloads were percent-encoded. Decoding the path with `urllib.parse.unquote` before matching, while
still displaying the raw value, raised the detection from 1 hit to 3 on the same file.

That is a small bug with a large lesson: half of log analysis is knowing what encoding you are looking
at.

## Limits

- Blunt regexes, not a WAF. It is a triage aid that tells you where to look; it will miss encoded or
  obfuscated payloads and it will occasionally false-positive on legitimate query strings.
- Combined-log format only.
- No time-window analysis, no correlation across files.

## Next version

- configurable pattern file instead of hard-coded regexes
- time-bucket summaries (requests per minute, to spot bursts)
- JSON output for piping into another tool

## License

MIT — see the repository [LICENSE](../../LICENSE).
