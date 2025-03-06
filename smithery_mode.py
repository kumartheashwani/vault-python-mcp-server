#!/usr/bin/env python3
"""
Smithery mode runner for the MCP server.
This script runs the server EXCLUSIVELY in stdio mode for Smithery integration.

IMPORTANT: This is the correct entry point for Smithery integration.
Using server.py directly will cause conflicts or timeouts as it
initiates both HTTP and stdio modes.
"""

import os
import sys
import asyncio
from server import handle_stdio_jsonrpc

if __name__ == "__main__":
    # Set the environment variable for stdio mode
    os.environ["MCP_STDIO_MODE"] = "1"
    
    # Create a new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    print("Starting MCP Calculator Server in EXCLUSIVE stdio mode for Smithery...", file=sys.stderr)
    
    try:
        # Run only the stdio handler, without starting the HTTP server
        loop.run_until_complete(handle_stdio_jsonrpc())
    finally:
        loop.close() 