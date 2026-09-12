#!/usr/bin/env python3
"""Agent discovery and distribution service."""
import json
import sqlite3
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

DB_PATH = "/tmp/discovery.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS agents (
        id TEXT PRIMARY KEY,
        uri TEXT,
        name TEXT,
        services TEXT,
        trust_score REAL DEFAULT 0.5,
        last_seen DATETIME
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS offers (
        id INTEGER PRIMARY KEY,
        agent_id TEXT,
        service TEXT,
        payment_info TEXT,
        timestamp DATETIME
    )''')
    conn.commit()
    conn.close()

init_db()

PAYMENT_INFO = {
    "address": "0xc5542FE4808263dFF01e7B519E29dbf57650E821",
    "chain": "base",
    "asset": "USDC",
    "amount": "0.10"
}

class DiscoveryHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def do_GET(self):
        if self.path == '/health':
            self.send_json({"status": "ok", "service": "discovery"})
        elif self.path == '/offer':
            self.send_json({
                "service": "text-toolkit",
                "price": PAYMENT_INFO,
                "endpoints": ["/v1/summarize", "/v1/keywords", "/v1/extract", "/v1/validate"],
                "description": "x402-gated text processing API"
            })
        elif self.path == '/agents':
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT * FROM agents")
            agents = [{"id": r[0], "name": r[2], "services": json.loads(r[3]) if r[3] else []} for r in c.fetchall()]
            conn.close()
            self.send_json({"agents": agents[:10]})
        else:
            self.send_json({"error": "Not found"}, 404)
    
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode() if length > 0 else '{}'
        data = json.loads(body) if body else {}
        
        if self.path == '/register':
            agent_id = data.get('agent_id')
            if agent_id:
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute("INSERT OR REPLACE INTO agents (id, uri, name, services, last_seen) VALUES (?, ?, ?, ?, ?)",
                          (agent_id, data.get('uri'), data.get('name'), json.dumps(data.get('services', [])), datetime.now().isoformat()))
                conn.commit()
                conn.close()
                self.send_json({"status": "registered"})
            else:
                self.send_json({"error": "agent_id required"}, 400)
        
        elif self.path == '/offer':
            agent_id = data.get('agent_id')
            service = data.get('service', 'text-toolkit')
            offer = {
                "service": service,
                "payment": PAYMENT_INFO,
                "contact": "0xc5542FE4808263dFF01e7B519E29dbf57650E821"
            }
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("INSERT INTO offers (agent_id, service, payment_info, timestamp) VALUES (?, ?, ?, ?)",
                      (agent_id, service, json.dumps(offer), datetime.now().isoformat()))
            conn.commit()
            conn.close()
            self.send_json({"status": "offer sent", "agent": agent_id})
        
        else:
            self.send_json({"error": "Not found"}, 404)

if __name__ == '__main__':
    port = int(__import__('sys').argv[1]) if len(__import__('sys').argv) > 1 else 8091
    print(f"Discovery service on port {port}")
    HTTPServer(('0.0.0.0', port), DiscoveryHandler).serve_forever()