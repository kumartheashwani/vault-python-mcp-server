#!/usr/bin/env python3
"""
Utility script to verify the server is running in the correct mode.
This script checks the environment variables and prints the current mode.
"""

import os
import sys
import argparse

def check_mode(args):
    """Check the current mode based on environment variables and command line arguments."""
    stdio_mode = os.environ.get("MCP_STDIO_MODE") == "1"
    http_mode = os.environ.get("MCP_HTTP_MODE") == "1"
    has_logging_config = args.logging_config
    
    if stdio_mode and http_mode:
        print("WARNING: Both MCP_STDIO_MODE and MCP_HTTP_MODE are set to 1.")
        print("This can cause conflicts. Please set only one of them.")
        return False
    
    if stdio_mode:
        print("Server is configured to run in stdio mode (MCP_STDIO_MODE=1).")
        print("This is the correct mode for Smithery local tool integration.")
        
        if not has_logging_config:
            print("\nWARNING: Missing required logging configuration flag.")
            print("For stdio mode, you must include the logging configuration flag:")
            print("  -Dlogging.config=classpath:logback-stdio.xml")
            return False
            
        print("Logging configuration is correctly set.")
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
    parser = argparse.ArgumentParser(description="Verify server mode configuration")
    parser.add_argument("--logging-config", action="store_true", default=False,
                        help="Flag to indicate if logging configuration is set")
    args = parser.parse_args()
    
    print("Checking server mode configuration...")
    success = check_mode(args)
    
    if not success:
        print("\nTo run in stdio mode for Smithery local tool integration:")
        print("  export MCP_STDIO_MODE=1  # On Unix/Linux/Mac")
        print("  set MCP_STDIO_MODE=1     # On Windows")
        print("  python -Dlogging.config=classpath:logback-stdio.xml server.py")
        print("\nOr use the provided scripts:")
        print("  ./start-smithery.sh      # On Unix/Linux/Mac")
        print("  start-smithery.bat       # On Windows")
        sys.exit(1)
    
    print("Mode configuration is correct.")
    sys.exit(0) 