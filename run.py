#!/usr/bin/env python3
"""
Auto-start and restart script for Text Toolkit API
"""
import subprocess
import os
import sys
import time

API_DIR = "/home/automaton/text-toolkit-api"
LOG_FILE = os.path.join(API_DIR, "logs", "server.log")
PID_FILE = os.path.join(API_DIR, "server.pid")

def start_server():
    # Ensure log directory exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    # Start server with nohup
    with open(LOG_FILE, 'a') as log_f:
        proc = subprocess.Popen(
            [sys.executable, "server.py", "8090"],
            stdout=log_f,
            stderr=log_f,
            cwd=API_DIR
        )
    
    with open(PID_FILE, 'w') as f:
        f.write(str(proc.pid))
    
    return proc.pid

if __name__ == "__main__":
    pid = start_server()
    print(f"Started Text Toolkit API with PID {pid}")
    print(f"Endpoints:")
    print(f"  /health - Free health check")
    print(f"  /v1/summarize - 0.10 USDC")
    print(f"  /v1/keywords - 0.10 USDC")
    print(f"  /v1/extract - 0.10 USDC")
    print(f"  /v1/validate - 0.10 USDC")
    print(f"  /v1/free-demo - Free (rate limited)")
    print(f"\nPayment address: 0xc5542FE4808263dFF01e7B519E29dbf57650E821 (USDC on Base)")