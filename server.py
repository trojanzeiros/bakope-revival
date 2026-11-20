
import os
import json
import socket
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

HOST = "0.0.0.0"
PORT = 8000

# ==========================================
# BAKOPE SUPABASE CONFIGURATION
# ==========================================

SUPABASE_URL = input("Supabase Project URL: ").strip().rstrip("/")
SUPABASE_KEY = input("Supabase Publishable API Key: ").strip()

if not SUPABASE_URL.startswith("https://"):
    raise SystemExit("Invalid Supabase URL.")

if not SUPABASE_KEY:
    raise SystemExit("Supabase API key is required.")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class BakopeHandler(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        super().end_headers()

    def do_GET(self):

        if self.path == "/":
            self.path = "/index.html"

        elif self.path == "/avatar":
            self.path = "/avatar.html"

        elif self.path == "/api/config":
            self.send_config()
            return

        return super().do_GET()

    def send_config(self):
        config = {
            "supabaseUrl": SUPABASE_URL,
            "supabaseKey": SUPABASE_KEY
        }

        data = json.dumps(config).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        print("[BAKOPE] " + (format % args))


def get_local_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.connect(("192.0.2.1", 80))
        return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        sock.close()


def main():

    if not os.path.isfile(os.path.join(BASE_DIR, "index.html")):
        raise SystemExit("index.html not found!")

    if not os.path.isfile(os.path.join(BASE_DIR, "avatar.html")):
        raise SystemExit("avatar.html not found!")

    server = ThreadingHTTPServer((HOST, PORT), BakopeHandler)

    ip = get_local_ip()

    print("\n" + "=" * 48)
    print("          BAKOPE LOCAL SERVER")
    print("=" * 48)
    print("[STATUS] Server running!")
    print("[LOCAL]  http://localhost:8000")
    print("[LAN]    http://" + ip + ":8000")
    print("[AVATAR] http://" + ip + ":8000/avatar")
    print("[API]    http://localhost:8000/api/config")
    print("=" * 48)
    print("Press CTRL+C to stop.\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[BAKOPE] Server stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
