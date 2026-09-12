#!/usr/bin/env python3
"""Text Toolkit API - Simple HTTP wrapper for text processing"""
import json, re
from http.server import HTTPServer, BaseHTTPRequestHandler

PAYMENT = "0xc5542FE4808263dFF01e7B519E29dbf57650E821"

class TT(BaseHTTPRequestHandler):
    def log(self, *args): pass
    def json(self, d, c=200):
        self.send_response(c)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(d, indent=2).encode())
    
    def do_GET(self):
        if self.path == '/health': self.json({'status': 'ok'})
        else: self.send_error(404)
    
    def do_POST(self):
        l = int(self.headers.get('Content-Length', 0))
        d = json.loads(self.rfile.read(l) or b'{}')
        t = d.get('text', '')
        if self.path == '/v1/summarize':
            self.json({'summary': t})
        elif self.path == '/v1/keywords':
            self.json({'keywords': re.findall(r'\w+', t.lower())[:10]})
        else: self.send_error(404)

if __name__ == '__main__':
    import sys
    HTTPServer(('0.0.0.0', int(sys.argv[1]) if len(sys.argv) > 1 else 8090), TT).serve_forever()