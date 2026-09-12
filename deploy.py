#!/usr/bin/env python3
"""
Text Toolkit API - Production deployment script
Starts the API server and configures auto-restart
"""
import subprocess
import os
import sys

def main():
    api_dir = "/home/automaton/text-toolkit-api"
    os.chdir(api_dir)
    
    # Start the server
    proc = subprocess.Popen(
        [sys.executable, "server.py", "8090"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=api_dir
    )
    
    print(f"Started Text Toolkit API: PID {proc.pid}")
    print(f"Health endpoint: curl http://localhost:8090/health")
    print(f"Payment address: 0xc5542FE4808263dFF01e7B519E29dbf57650E821")
    
    # Write PID file for management
    with open(f"{api_dir}/server.pid", "w") as f:
        f.write(str(proc.pid))

if __name__ == "__main__":
    main()