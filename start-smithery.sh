#!/bin/bash
# Start script for Smithery integration
# This script ensures the MCP server starts EXCLUSIVELY in stdio mode
# without launching the HTTP server

echo "Starting MCP Calculator Server in EXCLUSIVE stdio mode for Smithery..."
python smithery_mode.py 