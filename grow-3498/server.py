import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


for key in ("MANUAL_SECRET", "GENERATED_SECRET", "DEPLOYMENT_VERSION"):
    if not os.environ.get(key):
        raise SystemExit(f"Missing required environment variable: {key}")

body = (json.dumps({
    "fixture": "grow-3498",
    "version": os.environ["DEPLOYMENT_VERSION"],
    "serviceId": os.environ.get("RENDER_SERVICE_ID"),
    "commit": os.environ.get("RENDER_GIT_COMMIT"),
}) + "\n").encode()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


ThreadingHTTPServer(("0.0.0.0", int(os.environ.get("PORT", "10000"))), Handler).serve_forever()
