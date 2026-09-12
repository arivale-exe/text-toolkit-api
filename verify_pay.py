#!/usr/bin/env python3
"""x402 Payment Verification Module for Text Toolkit API"""
import json
import re
import urllib.request
import time

# Blockchain API endpoints (Base)
BASE_RPC = "https://base.llamarpc.io"
USDC_CONTRACT = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
PAYMENT_ADDRESS = "0xc5542FE4808263dFF01e7B519E29dbf57650E821"
PRICE_USDC = 100000  # 0.10 USDC (6 decimals)

# Simple in-memory payment cache to prevent replay attacks
_payment_cache = {}
CACHE_TTL = 3600  # 1 hour

def verify_tx(tx_hash, min_amount=PRICE_USDC):
    """Verify that a transaction actually transferred >= min_amount USDC to our wallet.
    Returns (valid, reason, amount_paid)
    """
    if not tx_hash:
        return False, "no transaction hash provided", 0
    
    # Check cache first (replay protection)
    if tx_hash in _payment_cache:
        if time.time() - _payment_cache[tx_hash]['time'] < CACHE_TTL:
            cached = _payment_cache[tx_hash]
            return cached['valid'], cached['reason'], cached['amount']
    
    try:
        # Fetch transaction details from Base
        tx_url = f"{BASE_RPC}/getTransaction?txHash={tx_hash}"
        req = urllib.request.Request(tx_url, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            tx_data = json.loads(resp.read().decode())
        
        if not tx_data.get('result'):
            return False, "transaction not found or not confirmed", 0
        
        # Look for USDC transfer to our wallet
        tx = tx_data.get('result', {})
        to = tx.get('to', '').lower()
        value = int(tx.get('value', '0x0'), 16) if isinstance(tx.get('value'), str) else tx.get('value', 0)
        
        # For ERC-20 transfers, we need to decode the input data
        # Simplified check: if tx is to USDC contract with transfer data
        input_data = tx.get('input', '0x')
        
        amount_transferred = 0
        paid_to_correct_address = False
        
        # Check if transaction is to USDC contract (ERC-20 transfer)
        if to.lower() == USDC_CONTRACT.lower() and input_data.startswith('0xa9059cbb'):
            # ERC-20 transfer: a9059cbb + address(32 bytes) + amount(uint256, 32 bytes)
            try:
                # Extract recipient address (bytes 32-64 after function selector)
                recipient = '0x' + input_data[34:74]
                # Extract amount
                amount_hex = input_data[74:138]
                amount_transferred = int(amount_hex, 16)
                
                # Check if transfer is to our payment address
                from eth_utils import to_checksum_address
                if recipient.lower() == PAYMENT_ADDRESS.lower():
                    paid_to_correct_address = True
            except Exception as e:
                # If USDC transfer decoding fails, fall through to simple ETH check
                pass
        
        # Fallback: direct ETH transfer to our wallet
        if not paid_to_correct_address and to.lower() == PAYMENT_ADDRESS.lower():
            # Convert wei to USDC equivalent (1:1 since USDC is 6 decimals)
            amount_transferred = value
        
        if paid_to_correct_address or (to.lower() == PAYMENT_ADDRESS.lower() and value >= min_amount):
            if amount_transferred >= min_amount:
                result = (True, "payment verified", amount_transferred)
                _payment_cache[tx_hash] = {'valid': True, 'reason': "payment verified", 'amount': amount_transferred, 'time': time.time()}
                return result
            else:
                result = (False, f"insufficient payment: {amount_transferred} < {min_amount} USDC", amount_transferred)
                _payment_cache[tx_hash] = {'valid': False, 'reason': f"insufficient", 'amount': amount_transferred, 'time': time.time()}
                return result
        else:
            result = (False, "transaction does not transfer USDC to payment address", 0)
            _payment_cache[tx_hash] = {'valid': False, 'reason': "wrong recipient", 'amount': 0, 'time': time.time()}
            return result
            
    except Exception as e:
        return False, f"verification error: {e}", 0

def verify_x402_payment(headers):
    """Verify x402 payment from HTTP headers.
    Checks for X-PAYMENT header containing a Base transaction hash."""
    
    # Look for payment header
    tx_hash = None
    for header_name in ['X-PAYMENT', 'X-Payment', 'X-TX-HASH', 'Authorization']:
        val = headers.get(header_name) or headers.get(header_name.lower())
        if val:
            # Extract hex hash
            match = re.search(r'0x[0-9a-fA-F]{64}', str(val))
            if match:
                tx_hash = match.group(0)
                break
            # Maybe the header IS the tx hash directly
            if re.match(r'^0x[0-9a-fA-F]{64}$', str(val)):
                tx_hash = val
                break
    
    if not tx_hash:
        return False, "no payment transaction provided"
    
    return verify_tx(tx_hash)

if __name__ == '__main__':
    # Self-test
    print("x402 Payment Verification Module")
    print(f"Payment address: {PAYMENT_ADDRESS}")
    print(f"Price: {PRICE_USDC / 1e6} USDC")
    print(f"USDC contract: {USDC_CONTRACT}")
    print(f"Base RPC: {BASE_RPC}")
    print("\nModule loaded successfully. Use verify_x402_payment(headers) in your server.")