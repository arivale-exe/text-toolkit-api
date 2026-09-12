#!/usr/bin/env python3
"""x402 Payment verification module for Base chain"""
import json
import urllib.request
from typing import Dict, Tuple, Optional

# Base chain configuration
BASE_RPC = "https://base-rpc.publicnode.com"
USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
WALLET = "0xc5542FE4808263dFF01e7B519E29dbf57650E821"
PRICE = 100000  # 0.10 USDC (6 decimals)

# Payment cache
_payments: Dict[str, dict] = {}

def verify_payment(tx_hash: str, max_price: int = PRICE) -> Tuple[bool, str, int]:
    """Verify x402 payment transaction on Base chain"""
    if not tx_hash:
        return False, "Missing transaction hash", 0
    
    if len(tx_hash) != 66 or not tx_hash.startswith('0x'):
        return False, "Invalid hash format", 0
    
    # Check cache
    if tx_hash in _payments:
        entry = _payments[tx_hash]
        return entry['valid'], entry['reason'], entry['amount']
    
    try:
        # Get transaction receipt
        payload = json.dumps({
            "jsonrpc": "2.0",
            "method": "eth_getTransactionReceipt",
            "params": [tx_hash],
            "id": 1
        }).encode()
        
        req = urllib.request.Request(BASE_RPC, data=payload, 
                                      headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode())
        
        receipt = result.get('result')
        if not receipt:
            return False, "Transaction not found", 0
        
        status = int(receipt.get('status', '0x0'), 16)
        if status != 1:
            return False, "Transaction failed", 0
        
        # Check for USDC transfer to our wallet
        amount = 0
        for log in receipt.get('logs', []):
            if log.get('address', '').lower() == USDC.lower():
                topics = log.get('topics', [])
                if len(topics) >= 3:
                    to_addr = '0x' + topics[2][-40:]
                    if to_addr.lower() == WALLET.lower():
                        amount = int(log.get('data', '0x0'), 16)
        
        valid = amount >= max_price
        _payments[tx_hash] = {'valid': valid, 'reason': 'verified' if valid else 'insufficient', 
                              'amount': amount, 'timestamp': __import__('time').time()}
        return valid, 'verified' if valid else f'insufficient: {amount}', amount
        
    except Exception as e:
        return False, f"Error: {e}", 0

def payment_required(resource: str = "/v1/summarize") -> dict:
    """Generate x402 payment request header"""
    return {
        "x402Version": 1,
        "accepts": [{
            "scheme": "exact",
            "network": "base",
            "maxAmountRequired": str(PRICE),
            "resource": "http://localhost:8090" + resource,
            "description": f"Text Toolkit API: {resource}",
            "payTo": WALLET,
            "asset": USDC,
            "chainId": 8453
        }],
        "error": "Payment required"
    }

if __name__ == '__main__':
    print("x402 Verification Module")
    print(f"Wallet: {WALLET}")
    print(f"USDC: {USDC}")
    print(f"Price: {PRICE/1e6} USDC")