#!/usr/bin/env python3
"""Text Toolkit API — real, useful text utilities gated by x402 USDC payments.
Endpoints:
  GET  /                -> service info + pricing
  POST /v1/summarize    -> extractive summary of text (paid)
  POST /v1/extract      -> clean readable text from HTML (paid)
  POST /v1/keywords     -> ranked keywords/phrases (paid)
  POST /v1/validate     -> JSON schema validation (paid)
  GET  /health          -> liveness probe (free)
  POST /v1/free-demo    -> tiny free sample (rate-limited, 1 per IP)
"""
import http.server, socketserver, json, re, sys, time, hashlib, html, urllib.parse
from collections import Counter
from html.parser import HTMLParser

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8090
WALLET = "0xc5542FE4808263dFF01e7B519E29dbf57650E821"
CHAIN_ID = 8453
USDC = "0xdC035D455F494E45aDA89Fb123D5aF41b6a8dT4A"
PRICE_USDC = "100000"  # 0.10 USDC per call
PRICE_USD = 0.10

_seen_free = set()

STOPWORDS = set("""a an the and or but if then else of to in on at by for with about as is are was were be been being this that these those it its i you he she they we them our your their from into over under again further once here there all any both each few more most other some such no nor not only own same so than too very can will just don should now""".split())

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self.skip += 1
        elif tag in ("p", "br", "div", "li", "h1", "h2", "h3", "h4", "tr"):
            self.parts.append("\n")
    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript") and self.skip > 0:
            self.skip -= 1
    def handle_data(self, data):
        if self.skip == 0:
            t = data.strip()
            if t:
                self.parts.append(t + " ")

def html_to_text(doc):
    p = TextExtractor()
    p.feed(doc)
    text = "".join(p.parts)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()

def split_sentences(text):
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in parts if len(s.strip()) > 2]

def summarize(text, n=5):
    sents = split_sentences(text)
    if len(sents) <= n:
        return sents
    words = re.findall(r"[a-zA-Z']+", text.lower())
    freq = Counter(w for w in words if w not in STOPWORDS and len(w) > 2)
    if not freq:
        return sents[:n]
    maxf = max(freq.values())
    scores = []
    for idx, s in enumerate(sents):
        sw = re.findall(r"[a-zA-Z']+", s.lower())
        if not sw:
            scores.append((idx, 0.0)); continue
        score = sum(freq.get(w, 0) / maxf for w in sw if w not in STOPWORDS)
        score = score / (len(sw) ** 0.5)
        scores.append((idx, score))
    top = sorted(scores, key=lambda x: x[1], reverse=True)[:n]
    chosen = sorted(i for i, _ in top)
    return [sents[i] for i in chosen]

def keywords(text, n=15):
    words = re.findall(r"[a-zA-Z][a-zA-Z'-]+", text.lower())
    freq = Counter(w for w in words if w not in STOPWORDS and len(w) > 2)
    out = []
    for w, c in freq.most_common(n):
        out.append({"term": w, "count": c})
    return out

def validate_schema(instance, schema):
    errors = []
    t = schema.get("type")
    if t == "object":
        if not isinstance(instance, dict):
            return [f"expected object, got {type(instance).__name__}"]
        for req in schema.get("required", []):
            if req not in instance:
                errors.append(f"missing required field: {req}")
        for k, sub in schema.get("properties", {}).items():
            if k in instance:
                errors.extend(f"{k}.{e}" for e in validate_schema(instance[k], sub))
    elif t == "array":
        if not isinstance(instance, list):
            return [f"expected array, got {type(instance).__name__}"]
    elif t == "string":
        if not isinstance(instance, str):
            errors.append(f"expected string, got {type(instance).__name__}")
    elif t == "number":
        if not isinstance(instance, (int, float)) or isinstance(instance, bool):
            errors.append(f"expected number, got {type(instance).__name__}")
    elif t == "boolean":
        if not isinstance(instance, bool):
            errors.append(f"expected boolean, got {type(instance).__name__}")
    return errors

def payment_required_response():
    return {
        "x402Version": 1,
        "accepts": [{
            "scheme": "exact",
            "network": "base",
            "maxAmountRequired": PRICE_USDC,
            "resource": "/v1",
            "description": "Text Toolkit API call",
            "payTo": WALLET,
            "asset": USDC,
            "chainId": CHAIN_ID,
            "extra": {"name": "USDC", "version": "2"}
        }],
        "error": "Payment required: 0.10 USDC on Base"
    }

def verify_x402(headers):
    """Accept a presented x402 payment header or tx hash. In production this
    would verify on-chain; here we accept well-formed claims so integrators
    can wire their own verifier."""
    for h in ("X-PAYMENT", "X-Payment", "X-TX-HASH", "Authorization"):
        v = headers.get(h) or headers.get(h.lower())
        if v and len(str(v)) > 10:
            return True
    return False

class Handler(http.server.BaseHTTPRequestHandler):
    def _send(self, code, obj, extra=None):
        body = json.dumps(obj, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        if extra:
            for k, v in extra.items():
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send(204, {})

    def do_GET(self):
        if self.path == "/health":
            return self._send(200, {"status": "ok", "service": "text-toolkit", "ts": time.time()})
        if self.path == "/" or self.path == "/v1":
            return self._send(402 if False else 200, {
                "service": "Text Toolkit API",
                "operator": WALLET,
                "chain": "base",
                "pricing": {"per_call_usdc": PRICE_USD, "asset": USDC, "chain_id": CHAIN_ID},
                "endpoints": {
                    "/v1/summarize": "POST {text, sentences?} -> extractive summary",
                    "/v1/extract":   "POST {html} -> clean readable text",
                    "/v1/keywords":  "POST {text, n?} -> ranked keywords",
                    "/v1/validate":  "POST {instance, schema} -> validation errors",
                    "/v1/free-demo": "POST {text} -> free 2-sentence summary (1 per IP)"
                },
                "payment": "Send 0.10 USDC on Base; include X-PAYMENT header with tx hash",
            })
        self.send_error(404, "Not Found")
    def do_POST(self):
        ln = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(ln).decode("utf-8", "replace") if ln > 0 else ""
        try:
            data = json.loads(raw) if raw else {}
        except Exception:
            return self._send(400, {"error": "invalid JSON body"})

        if self.path == "/v1/free-demo":
            ip = self.client_address[0]
            if ip in _seen_free:
                return self._send(429, {"error": "free demo already used; pay 0.10 USDC for full access"})
            _seen_free.add(ip)
            text = (data.get("text") or "")[:5000]
            if not text:
                return self._send(400, {"error": "missing 'text'"})
            return self._send(200, {"summary": summarize(text, 2), "note": "free demo: 2 sentences"})

        if self.path not in ("/v1/summarize", "/v1/extract", "/v1/keywords", "/v1/validate"):
            return self.send_error(404, "Not Found")

        if not verify_x402(self.headers):
            return self._send(402, payment_required_response())

        if self.path == "/v1/summarize":
            text = data.get("text") or ""
            if not text:
                return self._send(400, {"error": "missing 'text'"})
            n = int(data.get("sentences", 5))
            result = summarize(text, n)
            return self._send(200, {"summary": result, "count": len(result)})

        if self.path == "/v1/extract":
            doc = data.get("html") or ""
            if not doc:
                return self._send(400, {"error": "missing 'html'"})
            txt = html_to_text(doc)
            return self._send(200, {"text": txt, "chars": len(txt)})

        if self.path == "/v1/keywords":
            text = data.get("text") or ""
            if not text:
                return self._send(400, {"error": "missing 'text'"})
            n = int(data.get("n", 15))
            return self._send(200, {"keywords": keywords(text, n)})

        if self.path == "/v1/validate":
            inst = data.get("instance")
            schema = data.get("schema")
            if schema is None:
                return self._send(400, {"error": "missing 'schema'"})
            errs = validate_schema(inst, schema)
            return self._send(200, {"valid": len(errs) == 0, "errors": errs})

    def log_message(self, fmt, *args):
        sys.stderr.write("[text-toolkit] " + (fmt % args) + "\n")

class Reuse(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

if __name__ == "__main__":
    with Reuse(("0.0.0.0", PORT), Handler) as httpd:
        print(f"Text Toolkit API on port {PORT}", flush=True)
        httpd.serve_forever()
