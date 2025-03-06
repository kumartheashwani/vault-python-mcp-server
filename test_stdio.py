#!/usr/bin/env python3
import json
import subprocess
import time
import sys

def test_stdio_mode():
    """Test the server in stdio mode by sending JSON-RPC messages"""
    # Start the server process
    process = subprocess.Popen(
        [sys.executable, "server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={"MCP_STDIO_MODE": "1"},
        text=True,
        bufsize=1  # Line buffered
    )
    
    # Initialize request
    initialize_request = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "client_name": "test_client",
            "client_version": "1.0.0"
        },
        "id": 1
    }
    
    # Send initialize request
    process.stdin.write(json.dumps(initialize_request) + "\n")
    process.stdin.flush()
    
    # Read response
    initialize_response = json.loads(process.stdout.readline())
    print("Initialize Response:", json.dumps(initialize_response, indent=2))
    
    # List tools request
    list_tools_request = {
        "jsonrpc": "2.0",
        "method": "list_tools",
        "id": 2
    }
    
    # Send list tools request
    process.stdin.write(json.dumps(list_tools_request) + "\n")
    process.stdin.flush()
    
    # Read response
    list_tools_response = json.loads(process.stdout.readline())
    print("List Tools Response:", json.dumps(list_tools_response, indent=2))
    
    # Execute request
    execute_request = {
        "jsonrpc": "2.0",
        "method": "execute",
        "params": {
            "function_calls": [
                {
                    "name": "calculator",
                    "parameters": {
                        "operation": "add",
                        "numbers": [1, 2, 3]
                    }
                }
            ]
        },
        "id": 3
    }
    
    # Send execute request
    process.stdin.write(json.dumps(execute_request) + "\n")
    process.stdin.flush()
    
    # Read response
    execute_response = json.loads(process.stdout.readline())
    print("Execute Response:", json.dumps(execute_response, indent=2))
    
    # Shutdown request
    shutdown_request = {
        "jsonrpc": "2.0",
        "method": "shutdown",
        "id": 4
    }
    
    # Send shutdown request
    process.stdin.write(json.dumps(shutdown_request) + "\n")
    process.stdin.flush()
    
    # Read response
    shutdown_response = json.loads(process.stdout.readline())
    print("Shutdown Response:", json.dumps(shutdown_response, indent=2))
    
    # Wait for process to exit
    process.wait(timeout=5)
    
    print("All tests passed!")

if __name__ == "__main__":
    test_stdio_mode() 