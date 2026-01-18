#!/bin/bash
echo "================================================================"
echo "Starting SSH Tunnel via Pinggy.io (Reliable & Free)"
echo "================================================================"
echo "1. Wait for the URL (e.g., https://rand.a.pinggy.link)"
echo "2. Copy that URL."
echo "3. Add '/sse' to it."
echo "4. Update Athena."
echo "================================================================"

# pinggy.io (Free SSH tunnel)
ssh -o StrictHostKeyChecking=no -p 443 -R0:localhost:8000 a.pinggy.io
