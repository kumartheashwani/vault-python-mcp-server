#!/bin/bash
# Start script for Smithery integration
# This script uses the adaptive mode selection:
# - If stdin is available, it runs in stdio mode
# - If stdin is not available, it falls back to HTTP mode

echo "Starting MCP Calculator Server with adaptive mode selection..."
python smithery_mode.py 