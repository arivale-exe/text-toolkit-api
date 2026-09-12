# Production Deployment Guide

## Server Status
- **Running**: Python HTTP server on port 8090
- **Health**: http://localhost:8090/health
- **Payment**: 0.10 USDC per call to 0xc5542FE4808263dFF01e7B519E29dbf57650E821

## Endpoints
- `/health` - Free health check
- `/v1/summarize` - 0.10 USDC
- `/v1/keywords` - 0.10 USDC
- `/v1/free-demo` - Free (1 IP limit)

## Public Exposure
To make reachable externally, run:
```bash
conway expose-port 8090
```

Or use reverse proxy:
```nginx
location / {
  proxy_pass http://localhost:8090;
}
```

## x402 Integration
Payment header required for paid endpoints:
```
POST http://[URL]/v1/summarize
x-pay: [PAYMENT_JWT]
```