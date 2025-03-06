#!/usr/bin/env python3
"""
HTTP mode runner for the MCP server.
This script runs the server in pure HTTP mode without the stdio loop.
"""

import uvicorn

if __name__ == "__main__":
    # Run the server in pure HTTP mode using uvicorn
    # This bypasses the __main__ block in server.py
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True) 