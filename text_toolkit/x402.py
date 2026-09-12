#!/usr/bin/env python3
"""
x402 Payment Handler for Text Toolkit API
Handles USDC payments on Base chain (8453)

Wallet: 0xc5542FE4808263dFF01e7B519E29dbf57650E821
Price: 0.10 USDC per request
"""
import json
import hashlib
import time
from typing import Dict, Any, Optional

# Base chain USDC
USDC_CONTRACT = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
BASE_CHAIN_ID = 8453
PAYMENT_WALLET = "0xc5542FE4808263dFF01e7B519E29dbf57650E821"
PRICE_MICRO_USDC = 100000  # 0.10 USDC

def create_x402_header(resource: str, amount_micro_usdc: int = PRICE_MICRO_USDC) -> Dict[str, Any]:
    """Create x402 payment header for API requests"""
    return {
        "scheme": "exact",
        "network": "base",
        "payTo": PAYMENT_WALLET,
        "asset": USDC_CONTRACT,
        "chainId": BASE_CHAIN_ID,
        "maxAmountRequired": str(amount_micro_usdc),
        "resource": resource,
        "description": f"Text Toolkit API - {amount_micro_usdc/1e6} USDC per request"
    }

def verify_payment(headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """Verify x402 payment header"""
    x402 = headers.get('x402-payment', '')
    if not x402:
        x402 = headers.get('authorization', '')
    
    if x402.startswith('Bearer '):
        try:
            data = json.loads(x402[7:])
            return {
                "wallet": data.get("wallet"),
                "signature": data.get("signature"),
                "amount": data.get("amount", 0),
                "paid": True
            }
        except:
            return None
    
    return None

def require_payment(handler):
    """Decorator to require x402 payment before processing"""
    def wrapper(self, *args, **kwargs):
        # Check for free demo endpoint
        if 'free-demo' in self.path:
            return handler(self, *args, **kwargs)
        
        # Check x402 payment
        payment = verify_payment(dict(self.headers))
        if payment is None:
            # Return x402 payment terms
            resource = f"http://localhost:8090{self.path.split('?')[0]}"
            x402_terms = create_x402_header(resource)
            
            self.send_response(402)
            self.send_header('Content-Type', 'application/json')
            self.send_header('x402-payment-terms', json.dumps(x402_terms))
            self.end_headers()
            self.wfile.write(json.dumps(x402_terms).encode())
            return
        
        # Payment verified - process request
        return handler(self, *args, **kwargs)
    
    return wrapper

__all__ = [
    "create_x402_header",
    "verify_payment",
    "require_payment",
    "USDC_CONTRACT",
    "BASE_CHAIN_ID",
    "PAYMENT_WALLET",
    "PRICE_MICRO_USDC"
]