#!/usr/bin/env python3
"""
HTTP mode runner for the MCP server.
This script runs the server in pure HTTP mode without the stdio loop.
"""

import os
import uvicorn

# Set environment variable to ensure server.py only runs in HTTP mode
os.environ["MCP_HTTP_MODE"] = "1"

if __name__ == "__main__":
    # Run the server in pure HTTP mode using uvicorn
    # This bypasses the __main__ block in server.py
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False) 