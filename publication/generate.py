#!/usr/bin/env python3
"""Publication workflow for Text Toolkit API - generates discoverable artifacts"""
import json
import base64
import hashlib
from datetime import datetime

# Generate agent card for ERC-8004 registry
agent_card = {
    "name": "Text Toolkit",
    "description": "x402-gated text processing API - summarize, keywords, extract, validate",
    "authentication": None,  # No auth required
    "permissions": {},
    "endpoints": {
        "/health": {"method": "GET", "payment": "free"},
        "/v1/summarize": {"method": "POST", "payment": "0.10 USDC"},
        "/v1/keywords": {"method": "POST", "payment": "0.10 USDC"},
        "/v1/extract": {"method": "POST", "payment": "0.10 USDC"},
        "/v1/validate": {"method": "POST", "payment": "0.10 USDC"},
        "/v1/free-demo": {"method": "POST", "payment": "free (rate limited)"}
    },
    "contact": {
        "wallet": "0xc5542FE4808263dFF01e7B519E29dbf57650E821",
        "chain": "base"
    },
    "timestamp": datetime.utcnow().isoformat() + "Z"
}

# Generate publication artifacts
artifacts = {
    "agent_card": agent_card,
    "api_spec": {
        "openapi": "3.0.0",
        "info": {
            "title": "Text Toolkit API",
            "version": "1.0.0",
            "description": "Text processing API with x402 payments"
        },
        "servers": [{"url": "http://localhost:8090"}],
        "paths": {
            "/health": {
                "get": {"summary": "Health check", "responses": {"200": {"description": "OK"}}}
            }
        }
    },
    "deployment": {
        "port": 8090,
        "protocol": "x402",
        "payment_address": "0xc5542FE4808263dFF01e7B519E29dbf57650E821",
        "payment_token": "USDC",
        "payment_chain": "base"
    }
}

# Write artifacts
with open('/home/automaton/text-toolkit-api/publication/agent-card.json', 'w') as f:
    json.dump(agent_card, f, indent=2)

with open('/home/automaton/text-toolkit-api/publication/api-spec.json', 'w') as f:
    json.dump(artifacts['api_spec'], f, indent=2)

with open('/home/automaton/text-toolkit-api/publication/deployment.json', 'w') as f:
    json.dump(artifacts['deployment'], f, indent=2)

print("Publication artifacts generated successfully")
print("Ready for registration and distribution")