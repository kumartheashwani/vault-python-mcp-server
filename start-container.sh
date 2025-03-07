#!/bin/bash
# Start script for container deployments
# This script starts the server in HTTP mode for reliable API access

echo "Starting MCP Calculator Server in HTTP mode for container deployment..."

# Ensure logs directory exists
mkdir -p logs

# Set HTTP mode
export MCP_HTTP_MODE=1

# Start the server in HTTP mode
python http_server.py 