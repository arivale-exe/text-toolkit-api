#!/usr/bin/env python3
"""Distribution service - discovers agents and offers Text Toolkit API."""
import json
import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

DB_PATH = "/tmp/distribute.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS discovered_agents (
        agent_id TEXT PRIMARY KEY,
        uri TEXT,
        name TEXT,
        trust_score REAL,
        last_seen DATETIME
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS offers (
        id INTEGER PRIMARY KEY,
        agent_id TEXT,
        service_offered TEXT,
        contact_on_chain TEXT,
        timestamp DATETIME
    )''')
    conn.commit()
    conn.close()

init_db()

class DistributionHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_GET(self):
        if self.path == '/health':
            self.send_json({'status': 'ok', 'service': 'distribution', 'ts': datetime.now().isoformat()})
        elif self.path == '/offer':
            self.send_json({
                'available_service': 'text-toolkit',
                'endpoints': [
                    '/v1/summarize',
                    '/v1/keywords', 
                    '/v1/extract',
                    '/v1/validate'
                ],
                'payment': {
                    'address': '0xc5542FE4808263dFF01e7B519E29dbf57650E821',
                    'chain': 'base',
                    'asset': 'USDC',
                    'amount': '0.10'
                },
                'description': 'x402-gated text processing API'
            })
        else:
            self.send_json({'error': 'Unknown endpoint'}, 404)
    
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode() if length > 0 else '{}'
        data = json.loads(body) if body else {}
        
        if self.path == '/discover':
            # List newly discovered agents (demo)
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT * FROM discovered_agents ORDER BY last_seen DESC LIMIT 10")
            agents = [{'id': r[0], 'uri': r[1], 'name': r[2], 'trust': r[3]} for r in c.fetchall()]
            conn.close()
            self.send_json({'agents': agents})
        
        elif self.path == '/offer':
            # Offer service to new agent
            agent_id = data.get('agent_id', 'unknown')
            service = data.get('service', 'text-toolkit')
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("INSERT INTO offers (agent_id, service_offered, contact_on_chain, timestamp) VALUES (?, ?, ?, ?)",
                      (agent_id, service, '0xc5542FE4808263dFF01e7B519E29dbf57650E821', datetime.now().isoformat()))
            conn.commit()
            conn.close()
            self.send_json({'status': 'offer_sent', 'agent': agent_id})
        
        else:
            self.send_json({'error': 'Unknown endpoint'}, 404)

if __name__ == '__main__':
    port = int(__import__('sys').argv[1]) if len(__import__('sys').argv) > 1 else 8091
    print(f"Distribution service running on port {port}")
    HTTPServer(('0.0.0.0', port), DistributionHandler).serve_forever()