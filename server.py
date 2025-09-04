# C:\Users\baket\code\m2-miniweb\server.py
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).parent
WEB_DIR = ROOT / "web"

class RootHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Serve files from ./web
        if path == "/":
            path = "/index.html"
        return str(WEB_DIR / path.lstrip("/"))

if __name__ == "__main__":
    httpd = HTTPServer(("127.0.0.1", 8000), RootHandler)
    print("Serving on http://127.0.0.1:8000")
    httpd.serve_forever()
