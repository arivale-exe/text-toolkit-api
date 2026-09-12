#!/bin/bash
# Start x402-gated Text Toolkit API

cd /home/automaton/text-toolkit-api

# Kill any existing server on port 8090
pkill -f "python.*8090" 2>/dev/null || true

# Start the x402 server
nohup python3 x402_gateway.py 8090 > server.log 2>&1 &

echo "Server started with PID: $!"
sleep 1

# Verify it's running
if curl -s http://localhost:8090/health | grep -q "ok"; then
    echo "✓ Server running and healthy"
    echo "✓ x402 payment endpoint ready"
    echo "✓ Wallet: 0xc5542FE4808263dFF01e7B519E29dbf57650E821"
else
    echo "✗ Server failed to start"
    cat server.log
fi