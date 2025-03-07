# MCP Calculator Server

A Model Context Protocol (MCP) server implementation with a basic calculator tool. This server can be deployed in Smithery and provides arithmetic operations through a REST API.

## Features

- Basic arithmetic operations (add, subtract, multiply, divide)
- MCP-compliant API endpoints
- JSON schema validation
- Error handling
- Multiple communication modes (HTTP, WebSocket, stdio)
- Specialized entry points for different deployment scenarios

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

### HTTP Mode (Recommended for Production & Containers)

Run the server in pure HTTP mode using uvicorn directly:

```bash
# Set environment variable to ensure only HTTP mode runs
export MCP_HTTP_MODE=1  # On Windows: set MCP_HTTP_MODE=1
uvicorn server:app --host 0.0.0.0 --port 8000
```

Or use the provided script:

```bash
# On Unix/Linux/Mac
./start-container.sh

# On Windows
start-container.bat
```

This mode is recommended for:
- Production deployments
- Container environments
- Any scenario where reliable HTTP endpoints are required

### Smithery Mode (Local Tool Integration)

For Smithery integration as a local tool, use the stdio mode:

```bash
# Set environment variable to ensure only stdio mode runs
export MCP_STDIO_MODE=1  # On Windows: set MCP_STDIO_MODE=1
python server.py
```

Or use the provided convenience scripts:

```bash
# On Unix/Linux/Mac
./start-smithery.sh

# On Windows
start-smithery.bat
```

This mode is specifically designed for Smithery's local tool integration and communicates via standard input/output.

> **IMPORTANT**: Do NOT use `python server.py` without setting environment variables as it starts both HTTP and stdio modes simultaneously, which can cause conflicts or timeouts.

### Dual Mode (Development Only)

For development and testing both interfaces simultaneously:

```bash
# No environment variables set - runs both modes
python server.py
```

This starts both the HTTP server and stdio handler simultaneously, but may exit prematurely if stdin is closed. This mode is not recommended for production or Smithery integration.

## API Endpoints

### Standard Endpoints
- `GET /health`: Health check endpoint
- `GET /tools`: List available tools and their schemas
- `POST /`: JSON-RPC endpoint for MCP protocol
- WebSocket at `/`: WebSocket endpoint for MCP protocol

### Smithery Integration Endpoints
- `POST /mcp`: Dedicated MCP-compatible JSON-RPC endpoint for Smithery integration
- WebSocket at `/mcp`: Dedicated MCP-compatible WebSocket endpoint for Smithery integration

These dedicated MCP endpoints are specifically designed for Smithery integration and automatically handle initialization and tool listing without requiring explicit initialization steps.

## Using the Calculator Tool

### REST API

Example request to the `/tools` endpoint:

```bash
curl -X GET http://localhost:8000/tools
```

### JSON-RPC (HTTP)

Example request to the JSON-RPC endpoint:

```bash
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "execute", "params": {"function_calls": [{"name": "calculator", "parameters": {"operation": "add", "numbers": [1, 2, 3, 4]}}]}, "id": 1}'
```

Available operations:
- `add`: Adds all numbers
- `subtract`: Subtracts subsequent numbers from the first number
- `multiply`: Multiplies all numbers
- `divide`: Divides the first number by all subsequent numbers

## Error Handling

The server provides clear error messages for:
- Invalid operations
- Division by zero
- Insufficient number of operands
- Invalid parameter types
- JSON-RPC protocol errors

## Deployment

### Docker Container

Build and run the Docker container:

```bash
docker build -t mcp-calculator-server .
docker run -p 8000:8000 mcp-calculator-server
```

The container uses `uvicorn` directly to ensure the HTTP server starts reliably with proper signal handling, making the API endpoints accessible at http://localhost:8000.

## Smithery Integration

### Local Tool Integration (stdio mode)

For Smithery integration as a local tool, you **must** use stdio mode with the required logging configuration:

```bash
# Set environment variable to ensure only stdio mode runs
export MCP_STDIO_MODE=1  # On Windows: set MCP_STDIO_MODE=1

# Run with the required logging configuration
python -Dlogging.config=classpath:logback-stdio.xml server.py
```

Or use the provided convenience scripts:

```bash
# On Unix/Linux/Mac
./start-smithery.sh

# On Windows
start-smithery.bat
```

Configure Smithery to use the server as a local tool:

```json
{
  "name": "calculator",
  "description": "A basic calculator that can perform arithmetic operations",
  "command": ["python", "-Dlogging.config=classpath:logback-stdio.xml", "server.py"],
  "env": {
    "MCP_STDIO_MODE": "1"
  },
  "type": "local"
}
```

This configuration ensures the server communicates via stdio when run by Smithery as a local tool and properly configures the logging system.

> **IMPORTANT**: For local tool integration, you must use stdio mode (MCP_STDIO_MODE=1) with the logging configuration flag. HTTP mode will not work for local tool integration.

### Remote Tool Integration (HTTP mode)

For Smithery integration as a remote tool (e.g., in a container), use HTTP mode with the dedicated MCP endpoint:

```json
{
  "name": "calculator",
  "description": "A basic calculator that can perform arithmetic operations",
  "url": "http://your-container-host:8000/mcp",
  "type": "remote"
}
```

This configuration ensures Smithery can access the tool's API endpoints over HTTP using the dedicated MCP-compatible endpoint.

For the most reliable operation in container environments, use uvicorn directly in your deployment configuration:

```json
{
  "name": "calculator",
  "description": "A basic calculator that can perform arithmetic operations",
  "command": ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"],
  "env": {
    "MCP_HTTP_MODE": "1"
  },
  "type": "remote"
}
```

This ensures proper signal handling and more reliable startup in container environments. 