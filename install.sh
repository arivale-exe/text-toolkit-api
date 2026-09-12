#!/bin/bash
# Install and start Text Toolkit API as a service
set -e
cd /home/automaton/text-toolkit-api
nohup python3 server.py 8090 > /var/log/text-toolkit.log 2>&1 &
echo $! > /var/run/text-toolkit.pid
sleep 1
curl -s http://localhost:8090/health || echo "Failed to start"
echo "Service started on port 8090"