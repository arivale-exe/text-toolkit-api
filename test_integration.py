#!/usr/bin/env python3
"""
Integration test for Text Toolkit API
Tests the full payment flow via x402 protocol
"""
import json
import time
import threading
import subprocess
import requests
import sys

API_URL = "http://localhost:8090"
WALLET = "0xc5542FE4808263dFF01e7B519E29dbf57650E821"

def start_server(port=8090):
    """Start the API server in background"""
    proc = subprocess.Popen(
        [sys.executable, "-m", "text_toolkit", "--port", str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(2)
    return proc

def test_health():
    """Test health endpoint"""
    resp = requests.get(f"{API_URL}/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "LIVE"
    assert data["wallet"] == WALLET
    assert data["price"] == "0.10 USDC via x402"
    print("✓ Health check passed")

def test_summarize():
    """Test summarize endpoint"""
    text = "Machine learning is a subset of artificial intelligence that uses data and algorithms to imitate human intelligence. The overall goal is to make computers perform tasks that would normally require human intelligence."
    
    # x402 payment header
    payment_header = {
        "scheme": "exact",
        "network": "base",
        "payTo": WALLET,
        "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "chainId": 8453,
        "maxAmountRequired": "100000",
        "resource": f"{API_URL}/v1/summarize",
        "description": "Text Toolkit API - 0.10 USDC"
    }
    
    resp = requests.post(
        f"{API_URL}/v1/summarize",
        json={"text": text},
        headers={"x402-payment": json.dumps(payment_header)}
    )
    
    assert resp.status_code == 200
    result = resp.json()
    assert "summary" in result
    print("✓ Summarize test passed")

def test_extract():
    """Test extract endpoint"""
    text = "Quantum computing leverages quantum mechanics including superposition and entanglement to process information."
    
    resp = requests.post(
        f"{API_URL}/v1/extract",
        json={"text": text},
        headers={"x402-payment": json.dumps({})}
    )
    
    assert resp.status_code == 200
    print("✓ Extract test passed")

def test_keywords():
    """Test keywords endpoint"""
    text = "Natural language processing enables computers to understand and generate human language through neural networks."
    
    resp = requests.post(
        f"{API_URL}/v1/keywords",
        json={"text": text},
        headers={"x402-payment": json.dumps({})}
    )
    
    assert resp.status_code == 200
    print("✓ Keywords test passed")

if __name__ == "__main__":
    print("=== Text Toolkit API Integration Tests ===\n")
    
    # Check if server is running
    try:
        requests.get(f"{API_URL}/", timeout=2)
    except:
        print("Server not running, starting it...")
        proc = start_server()
    
    try:
        test_health()
        test_summarize()
        test_extract()
        test_keywords()
        print("\n=== ALL TESTS PASSED ===")
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)