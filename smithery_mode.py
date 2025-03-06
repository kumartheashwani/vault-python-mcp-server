#!/usr/bin/env python3
"""
Smithery mode runner for the MCP server.
This script runs the server in stdio mode for Smithery integration.

IMPORTANT: This is the correct entry point for Smithery integration.
Using server.py directly will cause conflicts or timeouts as it
initiates both HTTP and stdio modes.
"""

import os
import sys
import server

if __name__ == "__main__":
    # Set the environment variable for stdio mode
    os.environ["MCP_STDIO_MODE"] = "1"
    
    # Start the server in stdio mode only (no HTTP server)
    server.start_stdio_mode() 