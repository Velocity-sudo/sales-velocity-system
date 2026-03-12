#!/bin/bash
# Wrapper for extract_client_data.py — avoids macOS Full Disk Access issues
cd /Users/niko/Desktop/Clientes/LuchoBranding
/usr/bin/python3 scripts/extract_client_data.py "$@"
