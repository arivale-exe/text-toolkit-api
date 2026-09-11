#!/bin/bash
# Durable keeper for Text Toolkit API + its public tunnel.
# Idempotent: safe to run every 10 minutes from heartbeat.
set -u
cd /home/automaton/artifacts/text-toolkit
LOG=keeper.log
CF=/home/automaton/bin/cloudflared

# 1) Ensure API server is up
if ! curl -s --max-time 4 http://localhost:8090/health >/dev/null 2>&1; then
  nohup python3 server.py 8090 >> server.log 2>&1 &
  echo $! > server.pid
  echo "$(date -u +%FT%TZ) restarted API server" >> "$LOG"
fi

# 2) Ensure cloudflared tunnel is up; capture/refresh the public URL
URL=""
if command -v pgrep >/dev/null 2>&1; then
  if ! pgrep -f "cloudflared tunnel --url" >/dev/null 2>&1; then
    rm -f /tmp/cf.log
    nohup "$CF" tunnel --url http://localhost:8090 --no-autoupdate >> /tmp/cf.log 2>&1 &
    echo "$(date -u +%FT%TZ) restarted cloudflared tunnel" >> "$LOG"
    for i in $(seq 1 40); do
      URL=$(grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' /tmp/cf.log 2>/dev/null | head -1)
      [ -n "$URL" ] && break
      sleep 1
    done
  else
    URL=$(grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' /tmp/cf.log 2>/dev/null | head -1)
  fi
fi

# 3) Persist current public URL so other tools can read it
if [ -n "$URL" ]; then
  echo "$URL" > public_url.txt
  echo "$(date -u +%FT%TZ) public URL: $URL" >> "$LOG"
fi

# Keep only last 200 log lines
tail -200 "$LOG" > "$LOG.tmp" 2>/dev/null && mv "$LOG.tmp" "$LOG" 2>/dev/null
exit 0
