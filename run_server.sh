#!/bin/bash
# Run the SynthFrame MCP Server using the virtual environment

# Ensure we are in the project root
cd "$(dirname "$0")"

# Check if venv exists
if [ -f "backend/venv/bin/python3" ]; then
    echo "Starting SynthFrame Server..."
    backend/venv/bin/python3 backend/server.py
else
    echo "Error: Virtual environment not found at backend/venv/"
    echo "Please run: python3 -m venv backend/venv && source backend/venv/bin/activate && pip install -r backend/requirements.txt"
    exit 1
fi
