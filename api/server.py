import json
import os
import base64
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = REPO_ROOT / "data" / "processed"/ "sms_records.json"
LOCK = threading.Lock() # thread lock for safe file operations
PORT = 8000

# Demo user for basic auth
VALID_USERS = {"admin": "secret"} #admin: username, secret:password

def load_transactions():
    try:
        if DATA_FILE.exists():
            with DATA_FILE.open("r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Failed to load JSON: {e}")
    return []


def save_transactions(txs):
    with LOCK:
        os_dir = DATA_FILE.parent
        os_dir.mkdir(parents=True, exist_ok=True)
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump(txs, f, indent=2, ensure_ascii=False)


def check_auth(header: str) -> bool:
    """Check Basic Auth header."""
    if not header or not header.startswith("Basic "):
        return False
    try:
        encoded = header.split(" ", 1)[1]
        decoded = base64.b64decode(encoded).decode("utf-8")
        username, password = decoded.split(":", 1)
        return VALID_USERS.get(username) == password
    except Exception:
        return False


class TransactionHandler(BaseHTTPRequestHandler):
    def _send(self, code=200, data=None):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8") if data else b""
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def _require_auth(self):
        if not check_auth(self.headers.get("Authorization")):
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="MoMoAPI"')
            self.end_headers()
            return False
        return True

    def do_GET(self):
        if not self._require_auth():
            return

        txs = load_transaction()
        print([t["id"]for t in txs])

        parsed = urlparse(self.path)
        path_parts = parsed.path.strip("/").split("/")
        txs = load_transactions()
        print(t["id"] for t in txs)

        if parsed.path.rstrip("/") == "/transactions":
            params = parse_qs(parsed.query)
            address = params.get("address", [None])[0]
            tid = params.get("transaction_id", [None])[0]

            filtered = txs
            if address:
                filtered = [t for t in filtered if t.get("address") == address]
            if tid:
                filtered = [t for t in filtered if str(t.get("transaction_id")) == str(tid)]

            self._send(200, filtered)
            return

        elif len(path_parts) == 2 and path_parts[0] == "transactions":
            tx = next((t for t in txs if str(t["id"]) == path_parts[1]), None)
            if tx:
                self._send(200, tx)
            else:
                self._send(404, {"error": "Not found"})
            return

        self._send(404, {"error": "Endpoint not found"})

    def do_POST(self):
        if not self._require_auth():
            return
        if self.path.rstrip("/") != "/transactions":
            self._send(404, {"error": "Endpoint not found"})
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            payload = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            self._send(400, {"error": "Invalid JSON"})
            return

        txs = load_transactions()
        payload["id"] = max((int(t["id"]) for t in txs), default=0) + 1
        txs.append(payload)
        save_transactions(txs)
        self._send(201, payload)

    def do_PUT(self):
        if not self._require_auth():
            return
        path_parts = self.path.strip("/").split("/")
        if len(path_parts) != 2 or path_parts[0] != "transactions":
            self._send(404, {"error": "Endpoint not found"})
            return

        tid = path_parts[1]
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            payload = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            self._send(400, {"error": "Invalid JSON"})
            return

        txs = load_transactions()
        updated = None
        for i, tx in enumerate(txs):
            if str(tx["id"]) == tid:
                payload["id"] = tx["id"]
                txs[i] = payload
                updated = payload
                break

        if not updated:
            self._send(404, {"error": "Not found"})
            return
            
        save_transactions(txs)
        self._send(200, updated)

    def do_DELETE(self):
        if not self._require_auth():
            return
        path_parts = self.path.strip("/").split("/")
        if len(path_parts) != 2 or path_parts[0] != "transactions":
            self._send(404, {"error": "Endpoint not found"})
            return

        tid = path_parts[1]
        txs = load_transactions()
        removed = None
        for i, tx in enumerate(txs):
            if str(tx["id"]) == tid:
                removed = txs.pop(i)
                break

        if not removed:
            self._send(404, {"error": "Not found"})
            return

        save_transactions(txs)
        self._send(200, {"deleted": removed})

if __name__ == "__main__":
    server = HTTPServer(("localhost", PORT), TransactionHandler)
    print("API running at http://localhost:8000 (Basic Auth: admin/secret)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.server_close()
