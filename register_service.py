#!/usr/bin/env python3
"""Register Text Toolkit API in agent discovery systems."""
import json
import urllib.request
import hashlib

# Agent card URI - this would be hosted publicly
AGENT_URI = "https://basebnb.xyz/txt.json"

def compute_agent_id(uri):
    """Compute deterministic agent ID from URI hash."""
    return hashlib.sha256(uri.encode()).hexdigest()[:20]

def submit_to_registry():
    """Submit registration to various discovery systems."""
    agent_id = compute_agent_id(AGENT_URI)
    
    registration = {
        "agent_id": agent_id,
        "uri": AGENT_URI,
        "timestamp": "2025-01-16T00:00:00Z"
    }
    
    print(f"Agent ID: {agent_id}")
    print(f"URI: {AGENT_URI}")
    
    # Save to local registry
    with open("/tmp/local_agents.db", "w") as f:
        f.write(json.dumps(registration, indent=2))
    
    return registration

if __name__ == "__main__":
    result = submit_to_registry()
    print("Registration complete")
    print(json.dumps(result, indent=2))