#!/usr/bin/env python3
"""Service keeper - monitors and restarts the Text Toolkit API."""
import subprocess
import time
import os
import signal
import sys

PID_FILE = "/tmp/text-toolkit.pid"
log_file = "/tmp/text-toolkit.log"

def start_service():
    """Start the Text Toolkit API in background."""
    proc = subprocess.Popen(
        ["python3", "/home/automaton/text-toolkit-api/api_server.py", "8090"],
        stdout=open(log_file, 'a'),
        stderr=subprocess.STDOUT,
        start_new_session=True
    )
    with open(PID_FILE, 'w') as f:
        f.write(str(proc.pid))
    return proc

def check_service():
    """Check if service is running."""
    if not os.path.exists(PID_FILE):
        return False
    try:
        pid = int(open(PID_FILE).read().strip())
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, ValueError, FileNotFoundError):
        return False

def main():
    if not check_service():
        proc = start_service()
        print(f"Started Text Toolkit API (PID: {proc.pid})")
    else:
        pid = int(open(PID_FILE).read().strip())
        print(f"Text Toolkit API already running (PID: {pid})")

if __name__ == "__main__":
    main()