# C:\Users\baket\code\m2-miniweb\server.py
from __future__ import annotations
import json
import argparse
import logging
import threading
from logging.handlers import RotatingFileHandler
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from typing import Tuple

# --- paths and logging -------------------------------------------------------
ROOT = Path(__file__).parent
WEB_DIR = ROOT / "web"
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

MAX_BYTES = 256_000  # ~250 KB per file
BACKUPS = 3

_logger = logging.getLogger("miniweb")
_logger.setLevel(logging.INFO)

_log_file = LOG_DIR / "web.log"
_handler = RotatingFileHandler(
    _log_file, maxBytes=MAX_BYTES, backupCount=BACKUPS, encoding="utf-8"
)
_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
_logger.addHandler(_handler)

def _log_info(msg: str, *args) -> None:
    _logger.info(msg, *args)

# --- HTTP handler ------------------------------------------------------------
class AppHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        # Bridge stdlib handler logging to our rotating logger
        _log_info("%s - " + fmt, self.address_string(), *args)

    def translate_path(self, path: str) -> str:
        # Serve static files from ./web; "/" maps to index.html
        if path == "/":
            path = "/index.html"
        return str(WEB_DIR / path.lstrip("/"))

    def do_GET(self) -> None:
        parsed = urlparse(self.path)

        # JSON API: /api/echo?msg=hello
        if parsed.path == "/api/echo":
            qs = parse_qs(parsed.query)
            msg = (qs.get("msg") or [""])[0]
            payload = {"msg": msg, "length": len(msg)}
            data = json.dumps(payload).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        # Otherwise serve static
        super().do_GET()

# --- server wiring & CLI -----------------------------------------------------
def make_server(host: str = "127.0.0.1", port: int = 8000) -> Tuple[HTTPServer, int]:
    httpd = HTTPServer((host, port), AppHandler)
    return httpd, httpd.server_port

def run(blocking: bool = True, host: str = "127.0.0.1", port: int = 8000):
    httpd, port = make_server(host=host, port=port)
    if blocking:
        print(f"Serving on http://{host}:{port}")
        httpd.serve_forever()
    else:
        t = threading.Thread(target=httpd.serve_forever, daemon=True)
        t.start()
        return httpd, port, t

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="miniweb", description="Tiny stdlib web app")
    p.add_argument("--host", default="127.0.0.1", help="Host interface (default: 127.0.0.1)")
    p.add_argument("--port", default=8000, type=int, help="Port (default: 8000)")
    return p

if __name__ == "__main__":
    args = _build_parser().parse_args()
    raise SystemExit(run(blocking=True, host=args.host, port=args.port))
