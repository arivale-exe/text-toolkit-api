#!/usr/bin/env python3
"""Comprehensive test suite for Text Toolkit API"""
import json
import urllib.request
import urllib.error
import sys

BASE = "http://localhost:8090"

def req(path, data=None, method="GET"):
    body = json.dumps(data).encode() if data else None
    u = BASE + path
    r = urllib.request.Request(u, data=body, method=method)
    if data: r.add_header('Content-Type', 'application/json')
    try:
        resp = urllib.request.urlopen(r, timeout=5)
        return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())
    except Exception as e:
        return 0, {"error": str(e)}

# Run tests
tests = [
    ("Health", "/health", 200),
    ("Service", "/", 200),
    ("Summarize", "/v1/summarize", 200, {"text": "test"}),
    ("Keywords", "/v1/keywords", 200, {"text": "machine learning ai"}),
    ("Extract", "/v1/extract", 200, {"text": "John Smith works at Google"}),
    ("Validate", "/v1/validate", 200, {"text": "valid text"}),
]

print("Testing Text Toolkit API...")
for t in tests:
    if len(t) == 3:
        status, result = req(t[0], t[2]) if "text" in str(t) else req(t[0])
    else:
        status, result = req(t[1], t[3] if len(t) > 3 else None)
    print(f"  [{status}] {t[1]}")

print("\nAll tests complete!")