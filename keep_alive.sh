#!/bin/bash
# keep_alive.sh - Ensures the Text Toolkit API survives restarts.
# If port 8090 is free, starts server.py; otherwise confirms it's alive.
cd /home/automaton/artifacts/text-toolkit
if ! curl -s http://127.0.0.1:8090/health >/dev/null 2>&1; then
  nohup python3 server.py 8090 > server.log 2>&1 &
  echo $! > server.pid
  echo "Restarted Text Toolkit API (PID $(cat server.pid))"
else
  echo "Text Toolkit API already running (PID $(cat server.pid 2>/dev/null))"
fi
