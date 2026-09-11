#!/usr/bin/env python3
"""Real on-chain x402 payment verification for Base mainnet.

Uses a public Base RPC over plain HTTPS (no web3 dependency). Verifies:
  1. tx exists and succeeded
  2. tx transferred USDC (Transfer event) to our wallet
  3. amount >= required price
  4. tx not already spent (replay protection via local ledger)

This makes the payment gate HONEST: a bogus header no longer works.
"""
import json, urllib.request, re, sqlite3, os, time

WALLET = "0xc5542FE4808263dFF01e7B519E29dbf57650E821".lower()
USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913".lower()  # USDC on Base mainnet
BASE_RPCS = [
    "https://mainnet.base.org",
    "https://base.llamarpc.com",
    "https://base-rpc.publicnode.com",
    "https://1rpc.io/base",
]
TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
LEDGER = os.path.expanduser("~/artifacts/text-toolkit/spent_tx.db")

def _rpc(method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    last = None
    for url in BASE_RPCS:
        try:
            req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=8) as r:
                d = json.loads(r.read().decode())
                if "result" in d:
                    return d["result"]
                last = d.get("error")
        except Exception as e:
            last = str(e)
            continue
    raise RuntimeError(f"all RPCs failed: {last}")

def _ledger():
    con = sqlite3.connect(LEDGER)
    con.execute("CREATE TABLE IF NOT EXISTS spent (tx TEXT PRIMARY KEY, ts REAL, amount INTEGER)")
    con.commit()
    return con

def is_spent(tx):
    con = _ledger()
    row = con.execute("SELECT 1 FROM spent WHERE tx=?", (tx.lower(),)).fetchone()
    con.close()
    return row is not None

def mark_spent(tx, amount):
    con = _ledger()
    con.execute("INSERT OR IGNORE INTO spent VALUES (?,?,?)", (tx.lower(), time.time(), amount))
    con.commit()
    con.close()

def verify_tx(tx_hash, required_units):
    """Return (ok: bool, reason: str, paid_units: int)."""
    tx = (tx_hash or "").strip()
    if not re.fullmatch(r"0x[0-9a-fA-F]{64}", tx):
        return False, "malformed tx hash", 0
    if is_spent(tx):
        return False, "tx already redeemed (replay)", 0
    try:
        rcpt = _rpc("eth_getTransactionReceipt", [tx])
    except Exception as e:
        return False, f"rpc error: {e}", 0
    if not rcpt:
        return False, "tx not found / not yet mined", 0
    if int(rcpt.get("status", "0x0"), 16) != 1:
        return False, "tx reverted", 0
    paid = 0
    for log in rcpt.get("logs", []):
        if (log.get("address", "").lower() == USDC
                and log.get("topics", [None])[0] == TRANSFER_TOPIC
                and len(log["topics"]) >= 3):
            to_addr = "0x" + log["topics"][2][-40:].lower()
            if to_addr.lower() == WALLET:
                paid += int(log.get("data", "0x0"), 16)
    if paid == 0:
        return False, "no USDC transfer to operator in this tx", 0
    if paid < required_units:
        return False, f"underpaid: got {paid} units, need {required_units}", paid
    mark_spent(tx, paid)
    return True, "ok", paid

if __name__ == "__main__":
    import sys
    print(verify_tx(sys.argv[1] if len(sys.argv) > 1 else "", 100000))
