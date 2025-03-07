#!/usr/bin/env python3
"""
Utility script to verify the server is running in the correct mode.
This script checks the environment variables and prints the current mode.
"""

import os
import sys

def check_mode():
    """Check the current mode based on environment variables."""
    stdio_mode = os.environ.get("MCP_STDIO_MODE") == "1"
    http_mode = os.environ.get("MCP_HTTP_MODE") == "1"
    
    if stdio_mode and http_mode:
        print("WARNING: Both MCP_STDIO_MODE and MCP_HTTP_MODE are set to 1.")
        print("This can cause conflicts. Please set only one of them.")
        return False
    
    if stdio_mode:
        print("Server is configured to run in stdio mode (MCP_STDIO_MODE=1).")
        print("This is the correct mode for Smithery local tool integration.")
        return True
    
    if http_mode:
        print("Server is configured to run in HTTP mode (MCP_HTTP_MODE=1).")
        print("This is the correct mode for container deployments and remote tool integration.")
        print("For Smithery local tool integration, you should use stdio mode instead.")
        return False
    
    print("No mode is explicitly set. The server will run in dual mode.")
    print("This is not recommended for production or Smithery integration.")
    print("For Smithery local tool integration, set MCP_STDIO_MODE=1.")
    return False

if __name__ == "__main__":
    print("Checking server mode configuration...")
    success = check_mode()
    
    if not success:
        print("\nTo run in stdio mode for Smithery local tool integration:")
        print("  export MCP_STDIO_MODE=1  # On Unix/Linux/Mac")
        print("  set MCP_STDIO_MODE=1     # On Windows")
        print("  python server.py")
        print("\nOr use the provided scripts:")
        print("  ./start-smithery.sh      # On Unix/Linux/Mac")
        print("  start-smithery.bat       # On Windows")
        sys.exit(1)
    
    print("Mode configuration is correct.")
    sys.exit(0) 