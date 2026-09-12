#!/usr/bin/env python3
"""Text Toolkit API - Full Implementation with Working Endpoints"""
import json
import re
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import hashlib

PAYMENT_ADDRESS = "0xc5542FE4808263dFF01e7B519E29dbf57650E821"
USDC_CONTRACT = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
PRICE = 100000  # 0.10 USDC (6 decimals)

demo_usage = {}

def get_client_identifier(headers):
    """Get client identifier for rate limiting"""
    # Check for x-forwarded-for header (proxy)
    forwarded = headers.get('X-Forwarded-For')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return "127.0.0.1"

def summarize_text(text):
    """Simple text summarization - returns first 3 sentences"""
    sentences = text.split('.')
    summary = '. '.join(s.strip() for s in sentences[:3] if s.strip())
    return summary + ('.' if summary else '')

def extract_keywords(text, max_keywords=10):
    """Extract keywords - longer alpha words only"""
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    seen = {}
    for w in words:
        if w not in seen:
            seen[w] = 0
        seen[w] += 1
    # Sort by frequency, return top keywords
    sorted_words = sorted(seen.items(), key=lambda x: (-x[1], x[0]))
    return [w for w, c in sorted_words[:max_keywords]]

def extract_entities(text):
    """Extract named entities - capitalized words and common patterns"""
    # Simple entity extraction
    entity_patterns = [
        r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Proper nouns
        r'\b(?:https?://|www\.)[^\s]+\b',  # URLs
        r'\b\d{1,2}:\d{2}(?::\d{2})?\b',  # Times
        r'\b\d{4}\b',  # Years
        r'\b[\w\.-]+@[\w\.-]+\.\w+\b',  # Emails
    ]
    entities = set()
    for pattern in entity_patterns:
        matches = re.findall(pattern, text)
        entities.update(matches)
    return list(entities)[:20]

def validate_text(text):
    """Validate text and return analysis"""
    if not text:
        return {"valid": False, "error": "Text is required"}
    
    word_count = len(text.split())
    char_count = len(text)
    avg_word_len = sum(len(w) for w in text.split()) / max(1, word_count)
    
    has_upper = any(c.isupper() for c in text)
    has_digit = any(c.isdigit() for c in text)
    has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in text)
    
    return {
        "valid": True,
        "stats": {
            "words": word_count,
            "characters": char_count,
            "avg_word_length": round(avg_word_len, 2),
            "has_uppercase": has_upper,
            "has_digit": has_digit,
            "has_special": has_special
        }
    }

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # Suppress default logging
    
    def send_json(self, data, code=200):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def send_402(self, resource):
        self.send_response(402)
        self.send_header('Content-Type', 'application/json')
        self.send_header('x-pay', '0x')
        self.end_headers()
        offer = {
            "scheme": "exact", "network": "base", "maxAmountRequired": str(PRICE),
            "resource": resource, "description": f"{resource} (0.10 USDC)",
            "payTo": PAYMENT_ADDRESS, "asset": USDC_CONTRACT, "chainId": 8453,
            "extra": {"name": "USDC", "version": "2"}
        }
        response = {
            "x402Version": 1,
            "accepts": [offer],
            "error": "Payment required",
            "resource": resource
        }
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def do_GET(self):
        if self.path == '/health':
            self.send_json({
                "status": "ok",
                "service": "text-toolkit",
                "version": "1.0.0",
                "payment": "0.10 USDC per paid call"
            })
        else:
            self.send_error(404)
    
    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(length)) if length else {}
            text = data.get('text', '')
        except:
            text = ''
        
        client_id = get_client_identifier(self.headers)
        
        if self.path == '/v1/summarize':
            if text:
                self.send_json({"summary": summarize_text(text)})
            else:
                self.send_402('summarize')
        
        elif self.path == '/v1/keywords':
            if text:
                self.send_json({"keywords": extract_keywords(text)})
            else:
                self.send_402('keywords')
        
        elif self.path == '/v1/extract':
            if text:
                self.send_json({"entities": extract_entities(text)})
            else:
                self.send_402('extract')
        
        elif self.path == '/v1/validate':
            if text:
                self.send_json(validate_text(text))
            else:
                self.send_402('validate')
        
        elif self.path == '/v1/free-demo':
            if client_id not in demo_usage:
                demo_usage[client_id] = datetime.now().timestamp()
                self.send_json({
                    "summary": summarize_text(text),
                    "keywords": extract_keywords(text)
                })
            else:
                elapsed = datetime.now().timestamp() - demo_usage[client_id]
                if elapsed < 60:  # 1 minute cooldown
                    self.send_json({"error": "Rate limit: 1 request per minute"}, 429)
                else:
                    demo_usage[client_id] = datetime.now().timestamp()
                    self.send_json({
                        "summary": summarize_text(text),
                        "keywords": extract_keywords(text)
                    })
        
        else:
            self.send_error(404)

if __name__ == '__main__':
    port = int(os.sys.argv[1]) if len(os.sys.argv) > 1 else 8090
    print(f'Text Toolkit API v1.0.0')
    print(f'Port: {port}')
    print(f'Payment: 0.10 USDC | {PAYMENT_ADDRESS}')
    print(f'Endpoints:')
    print(f'  GET  /health         - Free health check')
    print(f'  POST /v1/summarize   - Get text summary')
    print(f'  POST /v1/keywords    - Extract keywords')
    print(f'  POST /v1/extract     - Extract entities')
    print(f'  POST /v1/validate    - Validate text')
    print(f'  POST /v1/free-demo   - Free demo (1/min)')
    HTTPServer(('0.0.0.0', port), Handler).serve_forever()