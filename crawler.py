#!/usr/bin/env python3
"""Fetch server version info from a third-party website.

This script sends a HEAD request (fallback to GET) and extracts
common server version headers such as Server and X-Powered-By.
"""

from __future__ import annotations

import argparse
import ssl
import sys
from typing import Iterable, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ServerVersionBot/1.0)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def request_headers(url: str, method: str) -> Tuple[int, Iterable[Tuple[str, str]]]:
    request = Request(url, method=method, headers=DEFAULT_HEADERS)
    context = ssl.create_default_context()
    with urlopen(request, timeout=10, context=context) as response:
        return response.status, response.getheaders()


def normalize_headers(headers: Iterable[Tuple[str, str]]) -> dict:
    normalized = {}
    for key, value in headers:
        normalized[key.lower()] = value
    return normalized


def fetch_server_info(url: str) -> dict:
    try:
        _, headers = request_headers(url, method="HEAD")
    except HTTPError as exc:
        headers = exc.headers.items()
    except URLError:
        _, headers = request_headers(url, method="GET")

    normalized = normalize_headers(headers)
    return {
        "server": normalized.get("server", "unknown"),
        "x_powered_by": normalized.get("x-powered-by", "unknown"),
        "via": normalized.get("via", "unknown"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch server version headers from a URL.")
    parser.add_argument("url", help="Target URL, e.g. https://example.com")
    args = parser.parse_args()

    try:
        info = fetch_server_info(args.url)
    except Exception as exc:  # pragma: no cover - top-level error handling
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print("Server:", info["server"])
    print("X-Powered-By:", info["x_powered_by"])
    print("Via:", info["via"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
