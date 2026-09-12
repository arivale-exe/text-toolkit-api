#!/usr/bin/env python3
import sys
import json
from .client import TextToolkitClient

def cli():
    if len(sys.argv) < 2:
        print("Usage: text-toolkit <command> [text]")
        print("Commands: summarize, keywords, extract, validate, info")
        sys.exit(1)
    
    client = TextToolkitClient()
    cmd = sys.argv[1]
    text = sys.argv[2] if len(sys.argv) > 2 else ""
    
    if cmd == "info":
        print(json.dumps(client.info(), indent=2))
    elif cmd == "summarize":
        print(json.dumps(client.summarize(text), indent=2))
    elif cmd == "keywords":
        print(json.dumps(client.keywords(text), indent=2))
    elif cmd == "extract":
        print(json.dumps(client.extract(text), indent=2))
    elif cmd == "validate":
        print(json.dumps(client.validate(text), indent=2))
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    cli()
