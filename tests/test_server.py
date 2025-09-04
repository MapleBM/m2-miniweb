# C:\Users\baket\code\m2-miniweb\tests\test_server.py
import json
import socket
import time
from urllib.request import urlopen
from urllib.error import URLError
import threading

import server

def _free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    _, port = s.getsockname()
    s.close()
    return port

def test_echo_returns_json():
    port = _free_port()
    httpd, _, t = server.run(blocking=False, port=port)
    try:
        # Wait briefly for server thread
        time.sleep(0.05)
        with urlopen(f"http://127.0.0.1:{port}/api/echo?msg=hi") as r:
            assert r.status == 200
            data = json.loads(r.read().decode("utf-8"))
            assert data == {"msg": "hi", "length": 2}
    finally:
        httpd.shutdown()

def test_serves_index_html():
    port = _free_port()
    httpd, _, t = server.run(blocking=False, port=port)
    try:
        time.sleep(0.05)
        with urlopen(f"http://127.0.0.1:{port}/") as r:
            assert r.status == 200
            html = r.read().decode("utf-8")
            assert "<title>M2 Miniweb</title>" in html
    finally:
        httpd.shutdown()
