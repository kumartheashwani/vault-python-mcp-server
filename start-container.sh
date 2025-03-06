#!/bin/bash
# Start script for container deployments
# This script starts the server in HTTP mode for reliable API access

echo "Starting MCP Calculator Server in HTTP mode for container deployment..."
export MCP_HTTP_MODE=1
uvicorn server:app --host 0.0.0.0 --port 8000 