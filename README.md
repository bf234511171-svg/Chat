# Server Version Crawler

Simple crawler script that fetches server version headers (e.g. `Server`, `X-Powered-By`) from a third-party website.

## Usage

```bash
python3 crawler.py https://example.com
```

## Notes

* The script prefers a `HEAD` request and falls back to `GET` if needed.
* Only headers are inspected; no page content is parsed.
