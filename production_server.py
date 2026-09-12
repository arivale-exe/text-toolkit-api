#!/usr/bin/env python3
"""Production Text Toolkit API with x402 payments"""
import json, re, os
from http.server import HTTPServer, BaseHTTPRequestHandler

PAYMENT_ADDRESS = "0xc5542FE4808263dFF01e7B519E29dbf57650E821"
PRICE_CENTS = 10  # 0.10 USDC
demo_hits = {}

class TTHandler(BaseHTTPRequestHandler):
    def log_message(self, *args): pass
    
    def send_json(self, data, code=200):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def send_402(self, resource):
        self.send_response(402)
        self.send_header('x-pay', '0x')
        self.end_headers()
        offer = {
            "scheme": "exact", "network": "base", "maxAmountRequired": "100000",
            "resource": resource, "payTo": PAYMENT_ADDRESS, "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
            "chainId": 8453, "extra": {"name": "USDC", "version": "2"}
        }
        self.wfile.write(json.dumps({"x402Version": 1, "accepts": [offer]}).encode())
    
    def do_GET(self):
        if self.path == '/health':
            self.send_json({"status": "ok", "payment": "0.10 USDC", "address": PAYMENT_ADDRESS})
        else: self.send_error(404)
    
    def do_POST(self):
        try:
            body = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0)) or b'{}'))
            text = body.get('text', '')
        except: text = ''
        
        ip = self.client_address[0]
        
        if self.path == '/v1/summarize': self.send_402('summarize')
        elif self.path == '/v1/keywords': self.send_402('keywords')
        elif self.path == '/v1/extract': self.send_402('extract')
        elif self.path == '/v1/validate': self.send_402('validate')
        elif self.path == '/v1/free-demo':
            if ip not in demo_hits:
                demo_hits[ip] = 1
                result = {'summary': '. '.join(text.split('.')[:3]), 'keywords': list(dict.fromkeys(re.findall(r'\b\w{4,}\b', text.lower())))[:10]}
                self.send_json(result)
            else:
                self.send_json({'error': 'Rate limited'}, 429)
        else: self.send_error(404)

if __name__ == '__main__':
    port = int(os.sys.argv[1]) if len(os.sys.argv) > 1 else 8090
    print(f'Production server: port {port}, payment: {PAYMENT_ADDRESS}')
    HTTPServer(('0.0.0.0', port), TTHandler).serve_forever()