# MCP Calculator Server

A Model Context Protocol (MCP) server implementation with a basic calculator tool. This server can be deployed in Smithery and provides arithmetic operations through a REST API.

## Features

- Basic arithmetic operations (add, subtract, multiply, divide)
- MCP-compliant API endpoints
- JSON schema validation
- Error handling
- Multiple communication modes (HTTP, WebSocket, stdio)
- Adaptive mode selection for flexible deployment

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

### Pure HTTP Mode (Recommended for Production)

Run the server in pure HTTP mode using uvicorn directly:

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

Or use the provided script:

```bash
python http_server.py
```

This mode is recommended for production deployments as it ensures the server runs reliably without the stdio loop.

### Adaptive Smithery Mode

For Smithery integration and container deployments, use the adaptive mode:

```bash
python smithery_mode.py
```

Or use the provided convenience scripts:

```bash
# On Unix/Linux/Mac
./start-smithery.sh

# On Windows
start-smithery.bat
```

This mode intelligently selects the appropriate communication method:
- If stdin is available (e.g., when run by Smithery as a local tool), it operates in stdio mode
- If stdin is not available (e.g., in container deployments), it automatically falls back to HTTP mode

This adaptive behavior ensures the server works correctly in all deployment scenarios.

> **IMPORTANT**: Do NOT use `python server.py` for Smithery integration as it starts both HTTP and stdio modes simultaneously, which can cause conflicts or timeouts.

### Dual Mode (Development Only)

For development and testing both interfaces simultaneously:

```bash
python server.py
```

This starts both the HTTP server and stdio handler simultaneously, but may exit prematurely if stdin is closed. This mode is not recommended for production or Smithery integration.

## API Endpoints

- `GET /health`: Health check endpoint
- `GET /tools`: List available tools and their schemas
- `POST /`: JSON-RPC endpoint for MCP protocol
- WebSocket at `/`: WebSocket endpoint for MCP protocol

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

### Docker

Build and run the Docker container:

```bash
docker build -t mcp-calculator-server .
docker run -p 8000:8000 mcp-calculator-server
```

The container will automatically start in HTTP mode since stdin is not available.

### Smithery

For Smithery deployment, configure the tool to use `smithery_mode.py` as the entry point:

```json
{
  "name": "calculator",
  "description": "A basic calculator that can perform arithmetic operations",
  "command": ["python", "smithery_mode.py"],
  "type": "local"
}
```

When run by Smithery as a local tool, the server will operate in stdio mode.
When deployed as a container, it will automatically fall back to HTTP mode if stdin is not available. 