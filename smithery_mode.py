#!/usr/bin/env python3
"""
Smithery mode runner for the MCP server.
This script runs the server in stdio mode for Smithery integration.
"""

import os
import sys
import server

if __name__ == "__main__":
    # Set the environment variable for stdio mode
    os.environ["MCP_STDIO_MODE"] = "1"
    
    # Start the server in stdio mode
    server.start_stdio_mode() 