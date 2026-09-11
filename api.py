#!/usr/bin/env python3
"""Main entry point for Text Toolkit API with x402 payment support."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from server import run_server
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Text Toolkit API Server")
    parser.add_argument("port", type=int, nargs="?", default=8090, help="Port to run server on")
    args = parser.parse_args()
    run_server(args.port)