"""
Verifier tests for dynamo/log-report.

Ground truth from environment/access.log (6 non-blank lines):
  192.168.0.1 GET /index.html   ×2
  192.168.0.2 GET /about.html   ×1
  192.168.0.2 GET /index.html   ×1
  10.0.0.5   POST /api/login   ×1
  10.0.0.5   GET  /about.html  ×1
  → total_requests = 6, unique_ips = 3, top_path = "/index.html" (3 hits)
"""
import json
from pathlib import Path

REPORT_PATH = Path("/app/report.json")

EXPECTED_TOTAL_REQUESTS = 6
EXPECTED_UNIQUE_IPS = 3
EXPECTED_TOP_PATH = "/index.html"


def test_report_structure():
    """Criterion 1: /app/report.json exists and contains valid JSON with keys
    total_requests, unique_ips, and top_path."""
    assert REPORT_PATH.exists(), (
        "Criterion 1 FAIL: /app/report.json does not exist"
    )
    content = REPORT_PATH.read_text().strip()
    assert content, "Criterion 1 FAIL: /app/report.json is empty"
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"Criterion 1 FAIL: not valid JSON — {exc}") from exc
    for key in ("total_requests", "unique_ips", "top_path"):
        assert key in data, f"Criterion 1 FAIL: missing key {key!r}"


def test_total_requests():
    """Criterion 2: total_requests equals the number of non-blank lines in the log."""
    data = json.loads(REPORT_PATH.read_text())
    assert data["total_requests"] == EXPECTED_TOTAL_REQUESTS, (
        f"Criterion 2 FAIL: expected total_requests={EXPECTED_TOTAL_REQUESTS}, "
        f"got {data['total_requests']!r}"
    )


def test_unique_ips():
    """Criterion 3: unique_ips equals the number of distinct client IP addresses."""
    data = json.loads(REPORT_PATH.read_text())
    assert data["unique_ips"] == EXPECTED_UNIQUE_IPS, (
        f"Criterion 3 FAIL: expected unique_ips={EXPECTED_UNIQUE_IPS}, "
        f"got {data['unique_ips']!r}"
    )


def test_top_path():
    """Criterion 4: top_path equals the URL path that appears in the most requests."""
    data = json.loads(REPORT_PATH.read_text())
    assert data["top_path"] == EXPECTED_TOP_PATH, (
        f"Criterion 4 FAIL: expected top_path={EXPECTED_TOP_PATH!r}, "
        f"got {data['top_path']!r}"
    )
