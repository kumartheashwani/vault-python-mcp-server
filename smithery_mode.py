#!/usr/bin/env python3
"""
Smithery mode runner for the MCP server.
This script intelligently selects the appropriate mode:
- If stdin is available, it runs in stdio mode for Smithery integration
- If stdin is not available, it falls back to HTTP mode for container deployments

IMPORTANT: This is the correct entry point for Smithery integration.
Using server.py directly will cause conflicts or timeouts as it
initiates both HTTP and stdio modes simultaneously.
"""

import os
import sys
import asyncio
import threading
import select
import time
from server import handle_stdio_jsonrpc, app

def is_stdin_available():
    """Check if stdin has data available or is connected to a pipe/terminal"""
    try:
        # Check if stdin is a TTY (terminal)
        if sys.stdin.isatty():
            return True
        
        # Check if stdin has data available
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        return bool(rlist)
    except:
        # If any error occurs, assume stdin is not available
        return False

def start_http_server():
    """Start the HTTP server"""
    import uvicorn
    print("No stdin detected. Starting in HTTP mode...", file=sys.stderr)
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)

def start_stdio_mode():
    """Start in stdio mode"""
    print("Stdin detected. Starting in EXCLUSIVE stdio mode...", file=sys.stderr)
    # Create a new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # Run only the stdio handler
        loop.run_until_complete(handle_stdio_jsonrpc())
    finally:
        loop.close()

if __name__ == "__main__":
    # Set the environment variable for stdio mode
    os.environ["MCP_STDIO_MODE"] = "1"
    
    # Check if stdin is available
    if is_stdin_available():
        # Start in stdio mode
        start_stdio_mode()
    else:
        # Fall back to HTTP mode if stdin is not available
        start_http_server() 