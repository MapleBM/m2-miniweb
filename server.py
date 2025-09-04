# C:\Users\baket\code\m2-miniweb\server.py
from __future__ import annotations
import json
import logging
import threading
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

        # API endpoint: /api/echo?msg=hello
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

        # Static: map "/" -> /web/index.html; else serve from /web
        self.serve_static(parsed.path)

    def translate_path(self, path: str) -> str:
        # Map HTTP path -> filesystem path under WEB_DIR
        if path == "/":
            path = "/index.html"
        return str(WEB_DIR / path.lstrip("/"))

    def serve_static(self, path: str) -> None:
        # Delegate to SimpleHTTPRequestHandler machinery
        super().do_GET()

def make_server(port: int = 8000) -> Tuple[HTTPServer, int]:
    # Build the HTTP server
    httpd = HTTPServer(("127.0.0.1", port), AppHandler)
    return httpd, httpd.server_port

def run(blocking: bool = True, port: int = 8000):
    httpd, port = make_server(port)
    if blocking:
        print(f"Serving on http://127.0.0.1:{port}")
        httpd.serve_forever()
    else:
        t = threading.Thread(target=httpd.serve_forever, daemon=True)
        t.start()
        return httpd, port, t

if __name__ == "__main__":
    run(blocking=True, port=8000)
