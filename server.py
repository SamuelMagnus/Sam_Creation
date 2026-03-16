"""
StockKeeper - Local USB Server
Serves the app and handles reading/writing inventory.json on the stick.
"""
import http.server
import json
import os
import sys
import webbrowser
import threading
import urllib.parse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "inventory.json")
APP_DIR   = os.path.join(BASE_DIR, "app")
PORT      = 17383   # obscure port, unlikely to clash


class Handler(http.server.BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass  # silence request logs

    # ── CORS + common headers ──────────────────────────────────
    def _send_headers(self, code=200, content_type="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

    def do_OPTIONS(self):
        self._send_headers(204)

    # ── GET ────────────────────────────────────────────────────
    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path

        # API: load inventory
        if path == "/api/load":
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = f.read()
            else:
                data = "[]"
            self._send_headers(200)
            self.wfile.write(data.encode("utf-8"))
            return

        # Serve app files
        if path == "/" or path == "":
            path = "/index.html"

        file_path = os.path.join(APP_DIR, path.lstrip("/"))
        if os.path.isfile(file_path):
            ext = os.path.splitext(file_path)[1].lower()
            mime = {
                ".html": "text/html; charset=utf-8",
                ".css":  "text/css",
                ".js":   "application/javascript",
                ".json": "application/json",
                ".png":  "image/png",
                ".ico":  "image/x-icon",
            }.get(ext, "text/plain")
            with open(file_path, "rb") as f:
                body = f.read()
            self._send_headers(200, mime)
            self.wfile.write(body)
        else:
            self._send_headers(404)
            self.wfile.write(b'{"error":"not found"}')

    # ── POST ───────────────────────────────────────────────────
    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path

        # API: save inventory
        if path == "/api/save":
            length = int(self.headers.get("Content-Length", 0))
            body   = self.rfile.read(length).decode("utf-8")
            try:
                json.loads(body)   # validate JSON
                os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    f.write(body)
                self._send_headers(200)
                self.wfile.write(b'{"ok":true}')
            except Exception as e:
                self._send_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return

        self._send_headers(404)
        self.wfile.write(b'{"error":"not found"}')


def open_browser():
    import time
    time.sleep(1.2)
    webbrowser.open(f"http://localhost:{PORT}")


if __name__ == "__main__":
    # Ensure data dir exists
    os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)

    server = http.server.HTTPServer(("localhost", PORT), Handler)
    print(f"\n  ╔══════════════════════════════════════╗")
    print(f"  ║   StockKeeper is running!            ║")
    print(f"  ║   http://localhost:{PORT}           ║")
    print(f"  ║                                      ║")
    print(f"  ║   Close this window to stop.         ║")
    print(f"  ╚══════════════════════════════════════╝\n")

    threading.Thread(target=open_browser, daemon=True).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
