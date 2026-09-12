#!/usr/bin/env python3
"""Text Toolkit API - Server Entry Point"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from text_toolkit.server import TextToolkitServer

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8090))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"Starting Text Toolkit API on {host}:{port}")
    print(f"Wallet: 0xc5542FE4808263dFF01e7B519E29dbf57650E821")
    print(f"Price: 0.10 USDC per request")
    TextToolkitServer.run(host=host, port=port)