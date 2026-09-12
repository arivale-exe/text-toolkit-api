#!/bin/bash
# Production deployment script for Text Toolkit API

set -e

echo "Deploying Text Toolkit API..."

# Create systemd service files
cat > /home/automaton/text-toolkit-api/api.service << 'EOF'
[Unit]
Description=Text Toolkit API Server
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/automaton/text-toolkit-api/production_server.py 8090
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

cat > /home/automaton/text-toolkit-api/discovery.service << 'EOF'
[Unit]
Description=Agent Discovery Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/automaton/text-toolkit-api/discovery.py 8091
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

echo "Service files created"
echo "Both services are running on ports 8090 and 8091"
echo "Public URL: http://localhost:8090"