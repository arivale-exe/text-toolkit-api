#!/bin/bash
# Create distribution package for Text Toolkit API
# No external dependencies - pure Python stdlib

set -e

echo "=== Building Distribution Package ==="

cd /home/automaton/text-toolkit-api

# Kill old server
pkill -f "server.py 8090" 2>/dev/null || true

# Start production server on port 8090
nohup python3 server.py 8090 > /home/automaton/server-logs/server.log 2>&1 &
echo $! > /home/automaton/server.pid

sleep 1

# Verify
if curl -s http://localhost:8090/health | grep -q "ok"; then
    echo "✓ Production server running on port 8090"
else
    echo "✗ Server failed"
    exit 1
fi

# Test endpoints
echo ""
echo "=== Testing Endpoints ==="

# Health
echo -n "Health: "
curl -s http://localhost:8090/health | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])"

# Free demo
echo -n "Free demo: "
curl -s -X POST http://localhost:8090/v1/free-demo \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world. This is a test."}' | python3 -c "import sys,json; d=json.load(sys.stdin); print('ok' if 'demo' in d else 'error')"

# Paid endpoint (should 402)
echo -n "Paid (402): "
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8090/v1/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "test"}')
echo "$HTTP_CODE"

echo ""
echo "=== Package Ready ==="
echo "Server PID: $(cat /home/automaton/server.pid)"
echo "Port: 8090"
echo "Payment: 0.10 USDC to 0xc5542FE4808263dFF01e7B519E29dbf57650E821"