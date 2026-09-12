#!/usr/bin/env python3
"""
x402 Payment Enforcement Module
Implements Base chain USDC payment verification for API endpoints
"""
import json
import time
import hashlib
import urllib.request
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass
from functools import wraps

# Chain configuration
BASE_RPC = "https://base-rpc.publicnode.com"
USDC_CONTRACT = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
WALLET_ADDRESS = "0xc5542FE4808263dFF01e7B519E29dbf57650E821"
CHAIN_ID = 8453  # Base mainnet

# Pricing
PRICE_USDC = 100000  # 0.10 USDC (6 decimals)

# Cache for replay protection (expiry: 1 hour)
_payment_cache: Dict[str, dict] = {}

@dataclass
class PaymentHeader:
    """Represents x402 payment header"""
    x402_version: int = 1
    network: str = "base"
    max_amount: int = PRICE_USDC
    resource: str = "/v1/summarize"
    pay_to: str = WALLET_ADDRESS
    asset: str = USDC_CONTRACT
    description: str = "Text Toolkit API call"
    
    def to_dict(self) -> dict:
        return {
            "x402Version": self.x402_version,
            "accepts": [{
                "scheme": "exact",
                "network": self.network,
                "maxAmountRequired": str(self.max_amount),
                "resource": "http://localhost:8090" + self.resource,
                "description": self.description,
                "payTo": self.pay_to,
                "asset": self.asset,
                "chainId": CHAIN_ID
            }],
            "error": "Payment required"
        }

def verify_transaction_on_chain(tx_hash: str) -> Tuple[bool, int, str]:
    """
    Verify transaction was successful on Base chain
    Returns: (is_success, usdc_amount, error_message)
    """
    if not tx_hash or len(tx_hash) != 66:
        return False, 0, "Invalid transaction hash"
    
    # Check cache first
    if tx_hash in _payment_cache:
        entry = _payment_cache[tx_hash]
        if time.time() - entry['timestamp'] < 3600:
            return entry['success'], entry['amount'], entry['reason']
    
    try:
        # Get transaction receipt
        payload = json.dumps({
            "jsonrpc": "2.0",
            "method": "eth_getTransactionReceipt",
            "params": [tx_hash],
            "id": 1
        }).encode('utf-8')
        
        req = urllib.request.Request(
            BASE_RPC,
            data=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        receipt = result.get('result')
        if not receipt:
            return False, 0, "Transaction not confirmed"
        
        # Check if successful
        status = int(receipt.get('status', '0x0'), 16)
        if status != 1:
            return False, 0, "Transaction reverted"
        
        # Look for USDC transfer to our wallet
        usdc_amount = 0
        for log in receipt.get('logs', []):
            if log.get('address', '').lower() == USDC_CONTRACT.lower():
                topics = log.get('topics', [])
                # Transfer event has: [topic0, from, to]
                if len(topics) >= 3:
                    to_addr = '0x' + topics[2][-40:] if len(topics[2]) >= 40 else topics[2]
                    if to_addr.lower() == WALLET_ADDRESS.lower():
                        usdc_amount = int(log.get('data', '0x0'), 16)
        
        # Cache result
        _payment_cache[tx_hash] = {
            'success': usdc_amount >= PRICE_USDC,
            'amount': usdc_amount,
            'reason': 'verified' if usdc_amount >= PRICE_USDC else 'insufficient amount',
            'timestamp': time.time()
        }
        
        return usdc_amount >= PRICE_USDC, usdc_amount, 'verified'
        
    except Exception as e:
        return False, 0, f"Verification error: {e}"

def generate_payment_challenge(endpoint: str = "/v1/summarize") -> str:
    """Generate JSON payment challenge for x402 header"""
    header = PaymentHeader(resource=endpoint)
    return json.dumps(header.to_dict(), indent=2)

def parse_payment_header(header_value: str) -> Optional[dict]:
    """Parse x402 payment header from request"""
    try:
        return json.loads(header_value)
    except:
        return None

def verify_payment(payment_header: Optional[dict], tx_hash: Optional[str]) -> Tuple[bool, str]:
    """
    Verify payment request
    Returns: (is_valid, message)
    """
    if not payment_header:
        return False, "No payment header provided"
    
    if not tx_hash:
        return False, "No transaction hash provided"
    
    # Verify chain matches
    accepts = payment_header.get('accepts', [])
    if not accepts:
        return False, "No payment accepts defined"
    
    for accept in accepts:
        if accept.get('network') != 'base':
            return False, f"Wrong network: {accept.get('network')}"
        
        if accept.get('payTo', '').lower() != WALLET_ADDRESS.lower():
            return False, "Payment not to our wallet"
        
        if int(accept.get('maxAmountRequired', '0')) > PRICE_USDC:
            return False, "Requested amount exceeds max"
    
    # Verify transaction on chain
    success, amount, reason = verify_transaction_on_chain(tx_hash)
    
    return success, reason

# Decorator for payment-required endpoints
def require_payment(endpoint: str):
    """Decorator to require payment for an endpoint"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check for X-PAYMENT header
            payment_header = kwargs.pop('payment_header', None)
            tx_hash = kwargs.pop('tx_hash', None)
            
            is_valid, message = verify_payment(payment_header, tx_hash)
            
            if not is_valid:
                return {
                    "error": "Payment required",
                    "status": 402,
                    "payment": generate_payment_challenge(endpoint),
                    "message": message
                }
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Convenience function
def get_payment_info() -> dict:
    """Get payment information for API discovery"""
    return {
        "wallet": WALLET_ADDRESS,
        "chain": "base",
        "chain_id": CHAIN_ID,
        "price": PRICE_USDC / 1000000,
        "price_usdc": PRICE_USDC,
        "asset": USDC_CONTRACT
    }

if __name__ == '__main__':
    # Print module info
    info = get_payment_info()
    print("x402 Payment Module")
    print(f"Wallet: {info['wallet']}")
    print(f"Chain: {info['chain']} (ID: {info['chain_id']})")
    print(f"Price: {info['price']} USDC")
    print(f"Asset: {info['asset']}")
    print("\nGenerating payment challenge for /v1/summarize:")
    print(generate_payment_challenge("/v1/summarize"))