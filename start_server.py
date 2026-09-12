#!/usr/bin/env python3
"""Start the Text Toolkit API server."""
import json
import subprocess
import sys

print("Starting Text Toolkit API server on port 8090...")

# Start server in background
proc = subprocess.Popen([
    sys.executable, '-m', 'http.server', '8090'
], cwd='/home/automaton/text-toolkit-api',
stdout=subprocess.DEVNULL,
stderr=subprocess.DEVNULL)

print(f"Server PID: {proc.pid}")
print("Server running on http://localhost:8090")