#!/usr/bin/env python3
"""Minimal x402-gated Text Toolkit API Server."""
import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

PAYMENT_INFO = {
    "x402Version": 1,
    "accepts": [{
        "scheme": "exact",
        "network": "base",
        "maxAmountRequired": "100000",
        "resource": "/v1",
        "description": "Text Toolkit API call",
        "payTo": "0xc5542FE4808263dFF01e7B519E29dbf57650E821",
        "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "chainId": 8453,
        "extra": {"name": "USDC", "version": "2"}
    }]
}

def summarize(text, n=3):
    """Extract n key sentences from text."""
    if not text:
        return []
    sentences = text.replace('!', '. ').replace('?', '. ').split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    if len(sentences) <= n:
        return sentences
    return sentences[:n]

def keywords(text, n=5):
    """Extract n keywords from text."""
    if not text:
        return []
    words = ''.join(c if c.isalnum() else ' ' for c in text).lower().split()
    keywords_list = [w for w in words if len(w) > 2]
    return list(dict.fromkeys(keywords_list))[:n]

def html_to_text(html):
    """Extract text from HTML."""
    if not html:
        return ""
    import re
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL|re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def validate(instance, schema):
    """Simple JSON Schema validation (basic implementation)."""
    if not schema:
        return []
    errors = []
    
    # Check required fields
    if 'required' in schema:
        for field in schema['required']:
            if field not in instance:
                errors.append(f"Missing required field: {field}")
    
    # Check type constraints
    if 'type' in schema:
        expected = schema['type']
        if expected == 'object' and not isinstance(instance, dict):
            errors.append(f"Expected object, got {type(instance).__name__}")
        elif expected == 'array' and not isinstance(instance, list):
            errors.append(f"Expected array, got {type(instance).__name__}")
        elif expected == 'string' and not isinstance(instance, str):
            errors.append(f"Expected string, got {type(instance).__name__}")
        elif expected == 'number' and not isinstance(instance, (int, float)):
            errors.append(f"Expected number, got {type(instance).__name__}")
    
    return errors

class APIHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_GET(self):
        if self.path == '/health':
            self.send_json({'status': 'ok', 'service': 'text-toolkit'})
        elif self.path == '/.well-known/x402/prepare':
            self.send_json(PAYMENT_INFO)
        else:
            self.send_json({'error': 'Not found'}, 404)
    
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode() if length > 0 else '{}'
        try:
            data = json.loads(body)
        except:
            self.send_json({'error': 'Invalid JSON'}, 400)
            return
        
        if self.path.startswith('/v1/summarize'):
            text = data.get('text', '')
            n = min(int(data.get('n', 3)), 10)
            self.send_json({'result': summarize(text, n)})
        
        elif self.path.startswith('/v1/keywords'):
            text = data.get('text', '')
            n = min(int(data.get('n', 5)), 20)
            self.send_json({'keywords': keywords(text, n)})
        
        elif self.path.startswith('/v1/extract'):
            html = data.get('html', '')
            self.send_json({'text': html_to_text(html)})
        
        elif self.path.startswith('/v1/validate'):
            instance = data.get('instance', {})
            schema = data.get('schema', {})
            errors = validate(instance, schema)
            self.send_json({'valid': len(errors) == 0, 'errors': errors})
        
        elif self.path.startswith('/v1/free-demo'):
            text = data.get('text', 'Hello world. This is a test.')
            result = summarize(text, 2)
            self.send_json({'result': result, 'note': 'free demo'})
        
        else:
            self.send_json(PAYMENT_INFO)

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8090
    HTTPServer(('0.0.0.0', port), APIHandler).serve_forever()