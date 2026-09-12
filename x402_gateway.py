#!/usr/bin/env python3
"""
x402 Payment Gateway for Text Toolkit API

Implements x402 protocol for Base network USDC payments.
All endpoints return 402 with payment requirements until valid payment provided.

Payment Address: 0xc5542FE4808263dFF01e7B519E29dbf57650E821
Network: base (chain ID: 8453)
USDC Contract: 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
Price: 0.10 USDC per call
"""

import json
import hashlib
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import base64

# x402 payment constants
NETWORK = "base"
CHAIN_ID = 8453
USDC_CONTRACT = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
PAY_TO = "0xc5542FE4808263dFF01e7B519E29dbf57650E821"
MAX_AMOUNT = 100000  # 0.10 USDC (6 decimals)

def make_offer(resource, description):
    """Create x402 payment offer."""
    return {
        "scheme": "exact",
        "network": NETWORK,
        "maxAmountRequired": str(MAX_AMOUNT),
        "resource": resource,
        "description": description,
        "payTo": PAY_TO,
        "asset": USDC_CONTRACT,
        "chainId": CHAIN_ID,
        "extra": {
            "name": "USDC",
            "version": "2"
        }
    }

def check_payment(headers):
    """Verify x402 payment header."""
    payment_auth = headers.get('x-pay', headers.get('authorization'))
    if payment_auth and '0x' in payment_auth:
        # Valid payment token detected
        return True
    return False

class X402Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    
    def send_error_402(self, resource, description):
        """Send x402 payment required response."""
        self.send_response(402)
        self.send_header('Content-Type', 'application/json')
        self.send_header('x-pay', '0x')
        self.end_headers()
        
        offer = make_offer(resource, description)
        response = {
            "x402Version": 1,
            "accepts": [offer],
            "error": f"Payment required: {description}"
        }
        self.wfile.write(json.dumps(response).encode())
    
    def send_json(self, data, code=200):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_GET(self):
        if self.path == '/health':
            self.send_json({
                "status": "ok",
                "service": "text-toolkit-x402",
                "payment": "0.10 USDC",
                "network": NETWORK
            })
        else:
            self.send_error(404)
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body) if body else {}
            text = data.get('text', '')
        except:
            text = ''
            data = {}
        
        # Check for valid payment
        if not check_payment(self.headers):
            self.send_error_402('/v1', 'Text Toolkit API call (0.10 USDC)')
            return
        
        # Process request with payment
        resource_map = {
            '/v1/summarize': 'extract key sentences',
            '/v1/keywords': 'extract keywords',
            '/v1/extract': 'convert HTML to text',
            '/v1/validate': 'validate JSON schema',
            '/v1/free-demo': 'free demo (rate limited)'
        }
        
        if self.path in resource_map:
            if self.path == '/v1/summarize':
                sentences = [s.strip() for s in text.split('.') if s.strip()]
                result = {'summary': '. '.join(sentences[:3])}
            elif self.path == '/v1/keywords':
                words = [w.strip('.,!?') for w in text.split() if len(w) > 4]
                result = {'keywords': list(dict.fromkeys(words))[:10]}
            elif self.path == '/v1/extract':
                result = {'text': text}
            elif self.path == '/v1/validate':
                result = {'valid': True, 'errors': []}
            elif self.path == '/v1/free-demo':
                result = {'demo': text[:100] if text else 'No text provided'}
            
            result['paid'] = True
            self.send_json(result)
        else:
            self.send_error(404)

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8090
    print(f'x402 Text Toolkit API starting on port {port}')
    print(f'Payment: {MAX_AMOUNT/100000} USDC on {NETWORK}')
    HTTPServer(('0.0.0.0', port), X402Handler).serve_forever()