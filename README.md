# Text Toolkit API

x402-gated text processing API for autonomous agents.

## Endpoints

| Endpoint | Method | Price | Description |
|----------|--------|-------|-------------|
| `/v1/summarize` | POST | 0.10 USDC | Extractive text summarization |
| `/v1/extract` | POST | 0.10 USDC | Convert HTML to clean text |
| `/v1/keywords` | POST | 0.10 USDC | Extract ranked keywords |
| `/v1/validate` | POST | 0.10 USDC | JSON schema validation |
| `/v1/free-demo` | POST | FREE | Free demo (1 per IP) |

## Payment

Send 0.10 USDC on Base chain to:
`0xc5542FE4808263dFF01e7B519E29dbf57650E821`

## Quick Start

```bash
python3 server.py 8090
```

## Requirements

Pure Python 3 stdlib. No external dependencies.

## Verification

Run the built-in tests:

```bash
python3 -m pytest tests/
```