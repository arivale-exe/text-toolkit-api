#!/usr/bin/env python3
"""Agent communication interface."""
import json
import urllib.request
from dataclasses import dataclass
from typing import Optional

@dataclass
class PaymentInfo:
    address: str
    chain: str
    asset: str
    amount: str
    chain_id: int

def x402_fetch(url: str, payment: PaymentInfo) -> dict:
    """Fetch URL with x402 payment."""
    # First request - expect 402
    req = urllib.request.Request(url, method='GET')
    
    def make_payment_request():
        # Sign payment with wallet (simulated)
        return {
            "x402Version": 1,
            "accepts": [{
                "scheme": "exact",
                "network": payment.chain,
                "maxAmountRequired": payment.amount.replace('.', ''),
                "resource": url,
                "payTo": payment.address,
                "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
                "chainId": payment.chain_id
            }]
        }
    
    try:
        # Try without payment first
        with urllib.request.urlopen(req, timeout=5) as resp:
            return {"status": "free", "data": json.loads(resp.read())}
    except Exception as e:
        return {"error": str(e)}

def validate_payment_response(resp_data: dict) -> bool:
    """Validate x402 payment response."""
    if 'x402Version' in resp_data:
        return True
    return False

def communicate_with_agent(agent_uri: str, message: dict) -> dict:
    """Send message to another agent via their endpoint."""
    try:
        req = urllib.request.Request(
            f"{agent_uri}/message",
            data=json.dumps(message).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return {"error": str(e)}

# Usage example
if __name__ == "__main__":
    payment = PaymentInfo(
        address="0xc5542FE4808263dFF01e7B519E29dbf57650E821",
        chain="base",
        asset="USDC",
        amount="0.10",
        chain_id=8453
    )
    
    print("Agent communication interface ready")
    print(f"Payment address: {payment.address}")
    print(f"Network: {payment.chain}:{payment.chain_id}")
    print(f"USDC amount: ${payment.amount}")