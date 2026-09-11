# Text Toolkit API

A lightweight, x402-gated text processing API built with Python's stdlib only.

## Endpoints

| Endpoint | Price | Description |
|----------|-------|-------------|
| `/v1/summarize` | 0.10 USDC | Extract key sentences from text |
| `/v1/keywords` | 0.10 USDC | Extract keywords from text |
| `/v1/extract` | 0.10 USDC | Convert HTML to plain text |
| `/v1/validate` | 0.10 USDC | Basic JSON Schema validation |
| `/v1/free-demo` | Free | Try summarization (1 call/IP) |
| `/health` | Free | Service health check |

## Payment

Payments are accepted via x402 protocol using USDC on Base chain.

- **Pay To**: `0xc5542FE4808263dFF01e7B519E29dbf57650E821`
- **Amount**: 0.10 USDC per call
- **Network**: Base (chainId 8453)
- **Asset*: USDC (0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913)

## Running

```bash
python3 api_server.py [port]
```

## GitHub

https://github.com/arivale-exe/text-toolkit-api