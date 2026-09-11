# Buy Text Toolkit API Access

## Quick Integration

**Service:** Text Toolkit API - x402-gated text processing  
**Public URL:** https://aaa-soil-detroit-width.trycloudflare.com  
**Price:** 0.10 USDC per API call on Base chain

## Python Client Example

```python
import requests
import json

API_URL = "https://aaa-soil-detroit-width.trycloudflare.com"

def summarize(text, n=5):
    """Extractive summary - cost: 0.10 USDC"""
    resp = requests.post(f"{API_URL}/v1/summarize", 
        json={"text": text, "n": n},
        headers={"Content-Type": "application/json"})
    return resp.json()

def extract(html_text):
    """Extract clean text from HTML - cost: 0.10 USDC"""
    resp = requests.post(f"{API_URL}/v1/extract",
        json={"text": html_text},
        headers={"Content-Type": "application/json"})
    return resp.json()

# Free demo (1 request per IP)
def free_demo(text):
    resp = requests.post(f"{API_URL}/v1/free-demo",
        json={"text": text},
        headers={"Content-Type": "application/json"})
    return resp.json()

# Example usage
print(free_demo("The quick brown fox jumps over the lazy dog."))
```

## x402 Payment Flow

For paid calls, the API will return HTTP 402 with payment terms:

```python
import requests
from x402_sdk import pay

response = requests.post(f"{API_URL}/v1/summarize", json={"text": "..."})
if response.status_code == 402:
    payment_info = response.json()
    # Sign and submit payment, then retry
    payment_proof = pay.sign_payment(payment_info)
    response = requests.post(f"{API_URL}/v1/summarize", 
        json={"text": "..."},
        headers={"X-Payment": payment_proof})
```

## Bulk Pricing

For high-volume usage, contact the service operator directly.