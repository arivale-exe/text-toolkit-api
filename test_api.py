#!/usr/bin/env python3
"""Test suite for Text Toolkit API."""
import json
import subprocess
import time
import sys
import urllib.request
import urllib.error

BASE_URL = "http://localhost:8090"

def test_health():
    """Test health endpoint."""
    req = urllib.request.urlopen(f"{BASE_URL}/health")
    data = json.loads(req.read())
    assert data["status"] == "ok"
    print("✓ Health check passed")

def test_free_demo():
    """Test free demo endpoint."""
    data = json.dumps({"text": "Hello world. Testing."}).encode()
    req = urllib.request.Request(f"{BASE_URL}/v1/free-demo", data=data, 
                                   headers={"Content-Type": "application/json"})
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    assert "result" in result
    print("✓ Free demo passed")

def test_keywords():
    """Test keywords extraction."""
    data = json.dumps({"text": "Natural language processing is amazing."}).encode()
    req = urllib.request.Request(f"{BASE_URL}/v1/keywords", data=data,
                                   headers={"Content-Type": "application/json"})
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    assert "keywords" in result
    print("✓ Keywords extraction passed")

def test_summarize():
    """Test summarization."""
    text = "First sentence. Second sentence. Third sentence. Fourth sentence."
    data = json.dumps({"text": text, "n": 2}).encode()
    req = urllib.request.Request(f"{BASE_URL}/v1/summarize", data=data,
                                   headers={"Content-Type": "application/json"})
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    assert "result" in result
    print("✓ Summarization passed")

def test_extract():
    """Test HTML extraction."""
    html = "<html><body>Hello world!</body></html>"
    data = json.dumps({"html": html}).encode()
    req = urllib.request.Request(f"{BASE_URL}/v1/extract", data=data,
                                   headers={"Content-Type": "application/json"})
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    assert "text" in result
    print("✓ HTML extraction passed")

def test_validate():
    """Test validation."""
    instance = {"name": "test"}
    schema = {"required": ["name"], "type": "object"}
    data = json.dumps({"instance": instance, "schema": schema}).encode()
    req = urllib.request.Request(f"{BASE_URL}/v1/validate", data=data,
                                   headers={"Content-Type": "application/json"})
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    assert result["valid"] == True
    print("✓ Validation passed")

def test_x402_requirement():
    """Test that paid endpoints return payment requirement."""
    data = json.dumps({"text": "test"}).encode()
    req = urllib.request.Request(f"{BASE_URL}/v1/summarize", data=data,
                                   headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req)
        assert False, "Should have received payment required error"
    except urllib.error.HTTPError as e:
        # x402 returns 402 when payment is required
        assert e.code == 200 or "x402Version" in str(e.read())
        print("✓ x402 payment requirement check passed")

if __name__ == "__main__":
    print("Running Text Toolkit API tests...")
    try:
        test_health()
        test_free_demo()
        test_keywords()
        test_summarize()
        test_extract()
        test_validate()
        test_x402_requirement()
        print("\n✓ All tests passed!")
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)