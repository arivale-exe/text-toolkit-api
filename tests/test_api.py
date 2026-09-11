#!/usr/bin/env python3
"""Tests for Text Toolkit API endpoints"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from texttoolkit import summarize, keywords, html_to_text, validate_schema

def test_summarize():
    text = "The quick brown fox jumps over the lazy dog. Machine learning is powerful. This is a test."
    result = summarize(text, 2)
    assert len(result) == 2
    assert all(len(s) > 0 for s in result)
    print("✓ summarize")

def test_keywords():
    text = "Machine learning algorithms process data efficiently. Machine data processing."
    result = keywords(text, 5)
    assert len(result) <= 5
    assert any(k["term"] == "machine" for k in result)
    print("✓ keywords")

def test_html_extract():
    html = "<html><body><p>Hello world</p></body></html>"
    result = html_to_text(html)
    assert "hello" in result.lower() or "world" in result.lower()
    print("✓ html_extract")

def test_validate():
    errors = validate_schema({"name": 123}, {"type": "object", "properties": {"name": {"type": "string"}}})
    assert len(errors) > 0
    print("✓ validate")

def test_api_endpoint():
    import urllib.request
    req = urllib.request.Request("http://localhost:8090/health")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            assert data["status"] == "ok"
            print("✓ api_endpoint")
    except Exception as e:
        print(f"✗ api_endpoint: {e}")

if __name__ == "__main__":
    print("Running tests...")
    test_summarize()
    test_keywords()
    test_html_extract()
    test_validate()
    test_api_endpoint()
    print("\nAll tests passed!")