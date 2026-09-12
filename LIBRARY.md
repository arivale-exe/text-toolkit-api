# Text Toolkit Library

## Usage Examples

### Python
```python
import requests

# Free demo
resp = requests.post('http://localhost:8090/v1/free-demo', 
    json={'text': 'Your text here'})
print(resp.json())

# Paid endpoint (requires x402 payment)
resp = requests.post('http://localhost:8090/v1/summarize',
    json={'text': 'Your text here'})
print(resp.json())
```

### cURL
```bash
# Free demo
curl -X POST http://localhost:8090/v1/free-demo \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello world"}'

# Paid (returns 402 with payment info)
curl -X POST http://localhost:8090/v1/summarize \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello world"}'
```

## Installation
```bash
# Clone and run
git clone https://github.com/automaton/text-toolkit-api
cd text-toolkit-api
python3 server.py 8090
```