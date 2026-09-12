#!/bin/bash
# Complete deployment and test script for Text Toolkit API

echo "=== Text Toolkit API - Complete Deployment ==="

# 1. Start API server
echo "1. Starting API server on port 8090..."
python3 /home/automaton/text-toolkit-api/production_server.py 8090 > /tmp/api.log 2>&1 &
API_PID=$!
echo "   PID: $API_PID"

# 2. Start discovery service
echo "2. Starting discovery service on port 8091..."
python3 /home/automaton/text-toolkit-api/discovery.py 8091 > /tmp/discovery.log 2>&1 &
DISC_PID=$!
echo "   PID: $DISC_PID"

sleep 2

# 3. Verify services
echo "3. Verifying services..."
API_HEALTH=$(curl -s http://localhost:8090/health)
DISC_HEALTH=$(curl -s http://localhost:8091/health)
echo "   API: $API_HEALTH"
echo "   Discovery: $DISC_HEALTH"

# 4. Run tests
echo "4. Running tests..."
python3 /home/automaton/text-toolkit-api/test_services.py

# 5. Test text processing
echo "5. Testing text processing..."
curl -s -X POST http://localhost:8090/v1/free-demo \
  -H "Content-Type: application/json" \
  -d '{"text": "First sentence. Second sentence. Third sentence."}'

echo ""
echo "=== Deployment Complete ==="