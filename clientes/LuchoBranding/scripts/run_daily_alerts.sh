#!/bin/bash
# Wrapper for daily_task_alerts.py — avoids macOS Full Disk Access issues
cd /Users/niko/Desktop/Clientes/LuchoBranding
/usr/bin/python3 scripts/daily_task_alerts.py "$@"
