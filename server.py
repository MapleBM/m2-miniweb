# C:\Users\baket\code\m2-miniweb\server.py
from __future__ import annotations
import json
import logging
import threading
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from typing import Tuple

ROOT = Path(__file__).parent
WEB_DIR = ROOT / "web"
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=str(LOG_DIR / "web.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

class AppHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        logging.info("%s - %s", self.address_string(), fmt % args)

    def do_GET(self):
        parsed = urlparse(self.path)

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

        # Serve static from ./web
        super().do_GET()

    def translate_path(self, path: str) -> str:
        if path == "/":
            path = "/index.html"
        return str(WEB_DIR / path.lstrip("/"))

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
