#!/usr/bin/env python3
"""Quick test of running services."""
import json
import urllib.request
import sys

def test_api():
    """Test API server on port 8090."""
    try:
        req = urllib.request.urlopen("http://localhost:8090/health", timeout=5)
        data = json.loads(req.read())
        print(f"✓ API on 8090: {data}")
        return True
    except Exception as e:
        print(f"✗ API on 8090: {e}")
        return False

def test_discovery():
    """Test discovery service on port 8091."""
    try:
        req = urllib.request.urlopen("http://localhost:8091/health", timeout=5)
        data = json.loads(req.read())
        print(f"✓ Discovery on 8091: {data}")
        return True
    except Exception as e:
        print(f"✗ Discovery on 8091: {e}")
        return False

def test_demo():
    """Test free demo endpoint."""
    try:
        data = json.dumps({"text": "Test summary."}).encode()
        req = urllib.request.Request(
            "http://localhost:8090/v1/free-demo",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=5)
        result = json.loads(resp.read())
        print(f"✓ Demo endpoint: {result}")
        return True
    except Exception as e:
        print(f"✗ Demo endpoint: {e}")
        return False

if __name__ == "__main__":
    print("Testing services...")
    results = [test_api(), test_discovery(), test_demo()]
    print(f"\n{sum(results)}/{len(results)} tests passed")
    sys.exit(0 if all(results) else 1)