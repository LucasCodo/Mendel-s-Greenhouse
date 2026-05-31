from __future__ import annotations

import sys
from pathlib import Path

EXPECTED_ARG_COUNT = 2
HTML_PATH_ARG = 1
CSP = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline' 'wasm-unsafe-eval' "
    "https://cdn.jsdelivr.net; "
    "connect-src 'self' https://cdn.jsdelivr.net; "
    "img-src 'self' data: blob:; "
    "style-src 'self' 'unsafe-inline'; "
    "font-src 'self' data:; "
    "worker-src 'self' blob:; "
    "object-src 'none'; "
    "base-uri 'none'; "
    "frame-ancestors 'self'"
)


def harden(html: str) -> str:
    body = html.removeprefix("<!doctype html>").strip()
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta
    http-equiv="Content-Security-Policy"
    content="{CSP}"
  >
  <title>Mendel's Greenhouse</title>
</head>
<body>
{body}
</body>
</html>
"""


def main() -> None:
    if len(sys.argv) != EXPECTED_ARG_COUNT:
        message = "Usage: harden_web_html.py <html-file>"
        raise SystemExit(message)
    html_path = Path(sys.argv[HTML_PATH_ARG])
    html_path.write_text(harden(html_path.read_text()), encoding="utf-8")


if __name__ == "__main__":
    main()
