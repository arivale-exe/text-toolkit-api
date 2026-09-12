#!/usr/bin/env python3
"""
Text Toolkit API Client
x402-gated text processing API client for AI agents

Wallet: 0xc5542FE4808263dFF01e7B519E29dbf57650E821
Chain: Base (8453)
Price: 0.10 USDC per request
"""
import json
import requests
from typing import Dict, Any, Optional

class X402PaymentError(Exception):
    """Raised when x402 payment terms cannot be met"""
    pass

class TextToolkitClient:
    """Client for x402-gated Text Toolkit API"""
    
    BASE_URL = "http://localhost:8090"
    WALLET = "0xc5542FE4808263dFF01e7B519E29dbf57650E821"
    USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    CHAIN_ID = 8453
    PRICE_MICRO_USDC = 100000  # 0.10 USDC
    
    def __init__(self, base_url: str = None, private_key: Optional[str] = None):
        self.base_url = base_url or self.BASE_URL
        self.private_key = private_key
    
    def _payment_header(self, endpoint: str) -> Dict[str, Any]:
        """Create x402 payment terms"""
        return {
            "scheme": "exact",
            "network": "base",
            "payTo": self.WALLET,
            "asset": self.USDC,
            "chainId": self.CHAIN_ID,
            "maxAmountRequired": str(self.PRICE_MICRO_USDC),
            "resource": f"{self.base_url}{endpoint}",
            "description": f"Text Toolkit API - 0.10 USDC per request"
        }
    
    def _request(self, endpoint: str, text: str) -> Dict[str, Any]:
        """Make a paid request to the API"""
        headers = {
            "Content-Type": "application/json",
            "x402-payment": json.dumps(self._payment_header(endpoint))
        }
        
        try:
            resp = requests.post(
                f"{self.base_url}{endpoint}",
                json={"text": text},
                headers=headers,
                timeout=30
            )
            
            if resp.status_code == 402:
                raise X402PaymentError("Payment required")
            
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.ConnectionError:
            raise X402PaymentError(f"Cannot connect to API at {self.base_url}")
    
    def summarize(self, text: str) -> str:
        """Summarize text via API"""
        result = self._request("/v1/summarize", text)
        return result.get("summary", text[:300])
    
    def extract(self, text: str) -> list:
        """Extract key concepts from text"""
        result = self._request("/v1/extract", text)
        return result.get("concepts", [])
    
    def keywords(self, text: str) -> list:
        """Extract keywords from text"""
        result = self._request("/v1/keywords", text)
        return result.get("keywords", [])
    
    def validate(self, text: str) -> dict:
        """Validate text format"""
        result = self._request("/v1/validate", text)
        return {"valid": result.get("valid", True)}

__all__ = ["TextToolkitClient", "X402PaymentError"]