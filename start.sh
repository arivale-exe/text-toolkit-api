#!/bin/bash
cd /home/automaton/text-toolkit-api
python3 -m http.server 8090 &
sleep 1
curl -s http://localhost:8090/
echo "Service started"