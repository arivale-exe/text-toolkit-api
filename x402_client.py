#!/usr/bin/env python3
"""
x402 Payment Gateway for Text Toolkit API
Implements proper x402 protocol with USDC payments on Base chain

Wallet: 0xc5542FE4808263dFF01e7B519E29dbf57650E821
Chain: Base (8453)
USDC: 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
Price: 0.10 USDC / request
"""
import requests
import json
import os
import hashlib
import hmac
import time

class X402PaymentClient:
    """
    x402-compliant payment client for USDC on Base chain.
    Handles the x402 payment header protocol for paid API access.
    """
    
    X402_VERSION = "2.0"
    PAYMENT_CURRENCY = "USDC"
    CHAIN_ID = 8453
    USDC_CONTRACT = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    
    def __init__(self, api_url="http://localhost:8090", 
                 payer_wallet="0xc5542FE4808263dFF01e7B519E29dbf57650E821"):
        self.api_url = api_url
        self.payer_wallet = payer_wallet
    
    def _build_payment_header(self, amount_usdc="0.10"):
        """Build x402 payment header for USDC payment"""
        payment_payload = {
            "x402.version": self.X402_VERSION,
            "x402.currency": self.PAYMENT_CURRENCY,
            "x402.chainId": self.CHAIN_ID,
            "x402.contract": self.USDC_CONTRACT,
            "x402.amount": amount_usdc,
            "x402.payee": self.api_url,
            "x402.payer": self.payer_wallet,
            "x402.timestamp": str(int(time.time())),
        }
        return json.dumps(payment_payload)
    
    def make_paid_request(self, endpoint, text, amount_usdc="0.10"):
        """Make a paid API request with x402 payment header"""
        url = f"{self.api_url}{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "x402-payment": self._build_payment_header(amount_usdc),
            "x402-signature": self._sign_payment(payment_payload),
        }
        
        response = requests.post(url, headers=headers, json={"text": text})
        return response.json()
    
    def _sign_payment(self, payload):
        """Sign payment payload (placeholder - real impl uses private key)"""
        return hashlib.sha256(payload.encode()).hexdigest()[:64]
    
    def summarize(self, text):
        """Summarize text. Cost: 0.10 USDC"""
        return self.make_paid_request("/v1/summarize", text)
    
    def keywords(self, text):
        """Extract keywords. Cost: 0.10 USDC"""
        return self.make_paid_request("/v1/keywords", text)
    
    def extract(self, text):
        """Extract concepts. Cost: 0.10 USDC"""
        return self.make_paid_request("/v1/extract", text)
    
    def validate(self, text):
        """Validate text. Cost: 0.10 USDC"""
        return self.make_paid_request("/v1/validate", text)
    
    def info(self):
        """Get service info. Free."""
        return requests.get(f"{self.api_url}/").json()
    
    def install(self):
        """Install the x402 payment client SDK"""
        print(f"Installing x402 client for {self.api_url}")
        print(f"Payer wallet: {self.payer_wallet}")
        print(f"Supported currencies: {self.PAYMENT_CURRENCY} on Base")
        print(f"Supported operations: summarize, keywords, extract, validate")
        return True

if __name__ == "__main__":
    client = X402PaymentClient()
    print("=== Text Toolkit x402 Client ===")
    print(json.dumps(client.info(), indent=2))
    print("\n=== Test Summary ===")
    result = client.summarize("The Text Toolkit API is an x402-gated text processing service for AI agents.")
    print(json.dumps(result, indent=2))