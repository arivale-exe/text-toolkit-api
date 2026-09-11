#!/usr/bin/env python3
"""
Discovery server for Text Toolkit API.
Lists available services for agent-to-agent discovery.
"""
import http.server, json, time, socketserver

PORT = 8093
WALLET = "0xc5542FE4808263dFF01e7B519E29dbf57650E821"

class DiscoveryHandler(http.server.BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send(204, {})

    def do_GET(self):
        if self.path == "/health":
            self._send(200, {"status": "ok", "service": "discovery", "ts": time.time()})
        elif self.path == "/offer":
            self._send(200, {
                "service": "Text Toolkit API",
                "operator": WALLET,
                "chain": "base",
                "description": "x402-gated text processing: summarize, extract, keywords, validate",
                "pricing": {"per_call_usdc": 0.10, "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", "chain_id": 8453},
                "endpoints": {
                    "summarize": "POST /v1/summarize",
                    "extract": "POST /v1/extract",
                    "keywords": "POST /v1/keywords",
                    "validate": "POST /v1/validate",
                    "free_demo": "POST /v1/free-demo"
                },
                "api_url": "http://localhost:8090",
                "docs": "https://arivale-exe.github.io/text-toolkit-api/"
            })
        elif self.path == "/manifest":
            self._send(200, {
                "name": "Text Toolkit API",
                "description": "x402-gated text processing API for autonomous agents",
                "version": "1.0.0",
                "author": WALLET,
                "chain": "Base",
                "payment": {"protocol": "x402", "amount": "0.10 USDC", "chain_id": 8453},
                "contact": {"github": "https://arivale-exe/text-toolkit-api"}
            })
        elif self.path == "/":
            self._send(200, {"message": "Discovery server for Text Toolkit API", "endpoints": ["/offer", "/health", "/manifest"]})
        else:
            self.send_error(404, "Not Found")

class ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

if __name__ == "__main__":
    server = ThreadingServer(("0.0.0.0", PORT), DiscoveryHandler)
    print(f"Discovery server running on port {PORT}")
    server.serve_forever()
