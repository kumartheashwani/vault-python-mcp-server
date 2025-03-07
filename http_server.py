#!/usr/bin/env python3
"""
HTTP mode runner for the MCP server.
This script runs the server in pure HTTP mode without the stdio loop.
"""

import os
import sys
import uvicorn
import logging
from loguru import logger

# Set environment variable to ensure server.py only runs in HTTP mode
os.environ["MCP_HTTP_MODE"] = "1"

# Configure logging
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add("logs/http-server.log", rotation="10 MB", level="DEBUG")

logger.info("Starting server in HTTP mode with auto-initialization")

try:
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Run the server in pure HTTP mode using uvicorn
    # This bypasses the __main__ block in server.py
    if __name__ == "__main__":
        logger.info("Launching uvicorn server on 0.0.0.0:8000")
        uvicorn.run(
            "server:app", 
            host="0.0.0.0", 
            port=8000, 
            reload=False,
            log_level="info",
            access_log=True
        )
except Exception as e:
    logger.exception(f"Error starting HTTP server: {e}")
    sys.exit(1) 