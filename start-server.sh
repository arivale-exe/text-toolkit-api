#!/bin/bash
# Auto-start script for Text Toolkit API
# Run as user: automaton

LOG_FILE="/home/automaton/text-toolkit-api/logs/server.log"
PID_FILE="/home/automaton/text-toolkit-api/server.pid"
API_DIR="/home/automaton/text-toolkit-api"

# Create log directory
mkdir -p "$(dirname "$LOG_FILE")"

# Check if already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "Already running with PID $PID"
        exit 0
    fi
fi

# Start server
cd "$API_DIR"
nohup python3 server.py 8090 >> "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"
echo "Started Text Toolkit API with PID $(cat $PID_FILE)"
echo "Exposed at: http://localhost:8090"