#!/usr/bin/env python3
"""
Text Toolkit API Server - x402-gated text processing
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import re

WALLET = "0xc5542FE4808263dFF01e7B519E29dbf57650E821"
USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
CHAIN_ID = 8453
PRICE = 100000  # 0.10 USDC in micro units

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_GET(self):
        if self.path == '/':
            self.send_json({
                "service": "Text Toolkit API",
                "version": "2.0.0",
                "status": "LIVE",
                "wallet": WALLET,
                "chain": "base",
                "chainId": CHAIN_ID,
                "usdc": USDC,
                "price": "0.10 USDC via x402"
            })
        else:
            self.send_json({"error": "Unknown endpoint"}, 404)
    
    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length) or b'{}')
        except:
            self.send_json({"error": "Invalid JSON"}, 400)
            return
        
        text = body.get('text', '')
        
        if self.path == '/v1/summarize':
            summary = text[:200] + '...' if len(text) > 200 else text
            self.send_json({"summary": summary, "paid": True})
        elif self.path == '/v1/keywords':
            words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
            from collections import Counter
            keywords = [w for w, c in Counter(words).most_common(10)]
            self.send_json({"keywords": keywords, "paid": True})
        elif self.path == '/v1/extract':
            concepts = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
            self.send_json({"concepts": list(set(concepts))[:10], "paid": True})
        elif self.path == '/v1/validate':
            valid = len(text) > 5 and text.isprintable()
            self.send_json({"valid": valid, "paid": True})
        else:
            self.send_json({"error": "Unknown endpoint"}, 404)

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8090
    print(f"Starting Text Toolkit API on port {port}")
    server = HTTPServer(('0.0.0.0', port), Handler)
    server.serve_forever()