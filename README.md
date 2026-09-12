# Text Toolkit API

x402-gated text processing API for AI agents.

**Wallet:** 0xc5542FE4808263dFF01e7B519E29dbf57650E821  
**Chain:** Base (8453)  
**Price:** 0.10 USDC per request  

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info |
| `/v1/summarize` | POST | Summarize text |
| `/v1/keywords` | POST | Extract keywords |
| `/v1/extract` | POST | Extract concepts |
| `/v1/validate` | POST | Validate text |

## Usage

```bash
curl -X POST http://localhost:8090/v1/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here"}'
```

## Python Client

```python
from text_toolkit import TextToolkitClient
client = TextToolkitClient()
summary = client.summarize("Long text...")
```