#!/bin/bash
# Start script for Smithery integration as a local tool
# This script starts the server in stdio mode for communication with Smithery

echo "Starting MCP Calculator Server in stdio mode for Smithery local tool integration..."
export MCP_STDIO_MODE=1
python server.py 