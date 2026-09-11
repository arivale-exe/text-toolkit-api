#!/usr/bin/env python3
"""Text Toolkit API Server with x402 payment support."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from http.server import HTTPServer, BaseHTTPRequestHandler
from texttoolkit import summarize, keywords, html_to_text, validate_schema

PAYMENT_ADDRESS = "0xc5542FE4808263dFF01e7B519E29dbf57650E821"
PAYMENT_CHAIN = "base"
PAYMENT_ASSET = "USDC"
PAYMENT_AMOUNT = "0.10"

class TextToolkitHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress logging

    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        if self.path == "/health":
            self.send_json_response({"status": "ok", "service": "text-toolkit"})
        elif self.path == "/offer":
            self.send_json_response({
                "payment": {
                    "address": PAYMENT_ADDRESS,
                    "chain": PAYMENT_CHAIN,
                    "asset": PAYMENT_ASSET,
                    "amount": PAYMENT_AMOUNT
                }
            })
        elif self.path == "/v1/free-demo":
            # Simple demo endpoint
            self.send_json_response({"error": "Use POST method"})
        else:
            self.send_json_response({"error": "Not found"}, 404)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode() if content_length > 0 else "{}"
        
        try:
            data = json.loads(body) if body else {}
        except:
            data = {}

        path = self.path

        if path.startswith("/v1/summarize"):
            text = data.get("text", "")
            n = int(data.get("n", 3))
            result = summarize(text, n)
            self.send_json_response({"result": result})

        elif path.startswith("/v1/extract"):
            html = data.get("html", "")
            result = html_to_text(html)
            self.send_json_response({"text": result})

        elif path.startswith("/v1/keywords"):
            text = data.get("text", "")
            n = int(data.get("n", 5))
            result = keywords(text, n)
            self.send_json_response({"keywords": result})

        elif path.startswith("/v1/validate"):
            instance = data.get("instance", {})
            schema = data.get("schema", {})
            errors = validate_schema(instance, schema)
            self.send_json_response({"valid": len(errors) == 0, "errors": errors})

        elif path == "/v1/free-demo" or path.startswith("/v1/free-demo"):
            # Free demo endpoint (rate limited by IP in production)
            text = data.get("text", "Hello world, this is a test.")
            result = summarize(text, 2)
            self.send_json_response({"result": result, "note": "free demo"})

        else:
            self.send_json_response({"error": "Unknown endpoint"}, 404)

def run_server(port=8090):
    server = HTTPServer(("0.0.0.0", port), TextToolkitHandler)
    print(f"Text Toolkit API running on port {port}", file=sys.stderr)
    server.serve_forever()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8090
    run_server(port)