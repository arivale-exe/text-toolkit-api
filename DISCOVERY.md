# Text Toolkit API - x402 Service Discovery

**Status:** Live and serving requests  
**Public URL:** https://aaa-soil-detroit-width.trycloudflare.com  
**Last updated:** 2026-09-11

## Payment Information

| Field | Value |
|-------|-------|
| Chain | Base (8453) |
| Asset | USDC (0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913) |
| Price | 0.10 USDC per API call |
| Wallet | 0xc5542FE4808263dFF01e7B519E29dbf57650E821 |

## Endpoints

| Endpoint | Method | Payment Required | Description |
|----------|--------|------------------|-------------|
| `/health` | GET | No | Liveness probe |
| `/v1` | GET | No | Service metadata |
| `/v1/free-demo` | POST | No (1/IP limit) | Free sample summary |
| `/v1/summarize` | POST | Yes (0.10 USDC) | Extractive summary (up to N sentences) |
| `/v1/extract` | POST | Yes (0.10 USDC) | HTML to clean text |
| `/v1/keywords` | POST | Yes (0.10 USDC) | Extract ranked keywords |
| `/v1/validate` | POST | Yes (0.10 USDC) | JSON schema validation |

## Request Format

All POST endpoints accept `application/json`:

```json
{
  "text": "Your text here",
  "n": 15          // optional, default varies by endpoint
}
```

## Payment

Include the tx hash in header: `X-Payment: 0x...`

Full x402 payment template for easy integration:

```json
{
  "x402Version": 1,
  "accepts": [
    {
      "scheme": "exact",
      "network": "base",
      "maxAmountRequired": "100000",
      "resource": "/v1",
      "description": "Text Toolkit API call",
      "payTo": "0xc5542FE4808263dFF01e7B519E29dbf57650E821",
      "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "chainId": 8453
    }
  ]
}
```