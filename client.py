#!/usr/bin/env python3
"""
x402 Client for Text Toolkit API
Automatically pays USDC on Base chain for API access
"""
import requests
import json
import os

class TextToolkitClient:
    """Client for the x402-gated Text Toolkit API"""
    
    def __init__(self, base_url="http://localhost:8090", wallet_address=None, private_key=None):
        self.base_url = base_url
        self.wallet_address = wallet_address
        self.private_key = private_key
    
    def _pay_and_request(self, endpoint, text):
        """Make a paid API request with x402 payment header"""
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        if self.wallet_address:
            headers["x402-payment"] = f"Wallet:{self.wallet_address}"
            headers["x402-config"] = json.dumps({
                "usdc": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
                "chainId": 8453,
                "price": "0.10USDC"
            })
        
        response = requests.post(url, headers=headers, json={"text": text})
        return response.json()
    
    def summarize(self, text):
        """Summarize text to key points. Cost: 0.10 USDC"""
        return self._pay_and_request("/v1/summarize", text)
    
    def keywords(self, text):
        """Extract top 10 keywords. Cost: 0.10 USDC"""
        return self._pay_and_request("/v1/keywords", text)
    
    def extract(self, text):
        """Extract named concepts. Cost: 0.10 USDC"""
        return self._pay_and_request("/v1/extract", text)
    
    def validate(self, text):
        """Validate text format. Cost: 0.10 USDC"""
        return self._pay_and_request("/v1/validate", text)
    
    def info(self):
        """Get service information. Free."""
        response = requests.get(self.base_url + "/")
        return response.json()

if __name__ == "__main__":
    client = TextToolkitClient()
    print("Service Info:", json.dumps(client.info(), indent=2))
    print("\nSummarization Result:", json.dumps(
        client.summarize("The Text Toolkit API provides x402-gated text processing services for AI agents. Each request costs 0.10 USDC on Base chain."),
        indent=2
    ))