#!/usr/bin/env python3
"""Register Text Toolkit API in ERC-8004 registry."""
import json
import hashlib

def compute_agent_id(uri):
    """Compute deterministic agent ID from URI hash."""
    return "0x" + hashlib.sha256(uri.encode()).hexdigest()[:20]

def register_agent():
    """Register agent in ERC-8004 registry."""
    agent_uri = "http://basebnb.xyz/txt.json"
    agent_id = compute_agent_id(agent_uri)
    
    agent_card = {
        "agentId": agent_id,
        "agentName": "TextToolkit",
        "agentType": "service",
        "description": "x402-gated text processing API on Base",
        "price": "0.10 USDC per call",
        "paymentAddress": "0xc5542FE4808263dFF01e7B519E29dbf57650E821",
        "endpoints": {
            "summarize": "/v1/summarize",
            "keywords": "/v1/keywords",
            "extract": "/v1/extract",
            "validate": "/v1/validate"
        },
        "network": "base",
        "asset": "USDC"
    }
    
    # Save to file for submission
    with open("/home/automaton/text-toolkit-api/agent_card.json", "w") as f:
        json.dump(agent_card, f, indent=2)
    
    print(f"Agent ID: {agent_id}")
    print(f"Agent card saved to: /home/automaton/text-toolkit-api/agent_card.json")
    
    return agent_card

if __name__ == "__main__":
    result = register_agent()
    print(json.dumps(result, indent=2))