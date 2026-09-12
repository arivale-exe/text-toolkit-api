# Text Toolkit API - Final Distribution Package

## Status: Live on port 8090

## API Endpoints

### GET /health
Free health check endpoint.

```bash
curl http://localhost:8090/health
```

### POST /v1/summarize
Paid endpoint: 0.10 USDC. Returns text summary (first 3 sentences).

### POST /v1/keywords
Paid endpoint: 0.10 USDC. Extracts keywords from text.

### POST /v1/extract
Paid endpoint: 0.10 USDC. Extracts named entities (URLs, emails, times, etc.).

### POST /v1/validate
Paid endpoint: 0.10 USDC. Validates text and returns statistics.

### POST /v1/free-demo
Free endpoint (rate limited: 1 request/minute/IP). Returns summary and keywords.

## Payment Information

**Address:** 0xc5542FE4808263dFF01e7B519E29dbf57650E821  
**Chain:** Base  
**Token:** USDC  
**Price:** 0.10 USDC per paid call

## x402 Payment Flow

1. Client calls paid endpoint
2. Server responds with 402 and payment offer
3. Client signs payment with their x402 wallet
4. Server verifies payment and processes request