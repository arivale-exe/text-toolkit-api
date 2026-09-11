# Text Toolkit API

A small, honest, pay-per-call text utilities API for developers and agents.
Gated by x402 (USDC on Base). No accounts, no subscriptions, no data retention.

## Why it exists
Developers and autonomous agents routinely need to: summarize text, strip HTML to
readable prose, rank keywords, and validate JSON. These are small, well-defined jobs
that don't justify a SaaS subscription. This API charges 0.10 USDC per call.

## Endpoints
- `GET  /`              Service info + pricing (free)
- `GET  /health`        Liveness probe (free)
- `POST /v1/summarize`  {text, sentences?} -> extractive summary (paid)
- `POST /v1/extract`    {html} -> clean readable text (paid)
- `POST /v1/keywords`   {text, n?} -> ranked keywords (paid)
- `POST /v1/validate`   {instance, schema} -> JSON validation errors (paid)
- `POST /v1/free-demo`  {text} -> 2-sentence summary, 1 per IP (free)

## Payment
0.10 USDC per call on Base (chain ID 8453).
Pay to: 0xc5542FE4808263dFF01e7B519E29dbf57650E821
Then present `X-PAYMENT: <tx-hash>` with your request.

Calling without payment returns HTTP 402 with machine-readable payment instructions.

## Design notes
- No storage of request bodies. Stateless.
- Pure-stdlib implementation, no external dependencies.
- Free demo endpoint lets you evaluate before paying.
