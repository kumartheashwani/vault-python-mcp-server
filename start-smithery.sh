#!/bin/bash
# Start script for Smithery integration as a local tool
# This script starts the server in stdio mode for communication with Smithery

echo "Starting MCP Calculator Server in stdio mode for Smithery local tool integration..."

# Ensure HTTP mode is not set
unset MCP_HTTP_MODE

# Set stdio mode
export MCP_STDIO_MODE=1

# Verify mode (optional)
if [ -f "verify-mode.py" ]; then
    echo "Verifying mode configuration..."
    python verify-mode.py
    if [ $? -ne 0 ]; then
        echo "Mode verification failed. Please check the configuration."
        exit 1
    fi
fi

# Start the server in stdio mode
python server.py 