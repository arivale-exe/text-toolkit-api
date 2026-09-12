#!/usr/bin/env python3
"""Text Toolkit API Client SDK for AI Agents
Python client for the x402-gated Text Toolkit API
Wallet: 0xc5542FE4808263dFF01e7B519E29dbf57650E821
Price: 0.10 USDC per request on Base chain
"""
import json
import urllib.request

class TextToolkitClient:
    def __init__(self, base_url="http://localhost:8090", wallet="0xc5542FE4808263dFF01e7B519E29dbf57650E821"):
        self.base_url = base_url
        self.wallet = wallet

    def summarize(self, text):
        return self._request("summarize", {"text": text})

    def keywords(self, text):
        return self._request("keywords", {"text": text})

    def extract(self, text):
        return self._request("extract", {"text": text})

    def validate(self, text):
        return self._request("validate", {"text": text})

    def info(self):
        req = urllib.request.Request(f"{self.base_url}/")
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())

    def _request(self, endpoint, data):
        req = urllib.request.Request(
            f"{self.base_url}/{endpoint}",
            data=json.dumps(data).encode(),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())

# Usage example
if __name__ == "__main__":
    client = TextToolkitClient()
    print("=== Service Info ===")
    print(json.dumps(client.info(), indent=2))
    print("\n=== Summarize ===")
    print(json.dumps(client.summarize("Text Toolkit API is x402-gated. Price 0.10 USDC per call."), indent=2))
    print("\n=== Keywords ===")
    print(json.dumps(client.keywords("This is a test sentence for the Text Toolkit API service"), indent=2))