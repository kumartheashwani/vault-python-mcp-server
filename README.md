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
uvicorn server:app --host 0.0.0.0 --port 8000
```

Or use the provided script:

```bash
python http_server.py
```

This mode is recommended for:
- Production deployments
- Container environments
- Any scenario where reliable HTTP endpoints are required

### Smithery Mode (Local Tool Integration)

For Smithery integration as a local tool, use the stdio mode:

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

This mode is specifically designed for Smithery's local tool integration and communicates via standard input/output.

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

### Docker Container

Build and run the Docker container:

```bash
docker build -t mcp-calculator-server .
docker run -p 8000:8000 mcp-calculator-server
```

The container uses `uvicorn` directly to ensure the HTTP server starts reliably with proper signal handling, making the API endpoints accessible at http://localhost:8000.

### Smithery Local Tool

For Smithery deployment as a local tool, configure it to use `smithery_mode.py`:

```json
{
  "name": "calculator",
  "description": "A basic calculator that can perform arithmetic operations",
  "command": ["python", "smithery_mode.py"],
  "type": "local"
}
```

This configuration ensures the server communicates via stdio when run by Smithery as a local tool.

### Smithery Remote Tool

For Smithery deployment as a remote tool (e.g., in a container), configure it to use HTTP mode:

```json
{
  "name": "calculator",
  "description": "A basic calculator that can perform arithmetic operations",
  "url": "http://your-container-host:8000",
  "type": "remote"
}
```

For the most reliable operation in container environments, use uvicorn directly in your deployment configuration:

```json
{
  "name": "calculator",
  "description": "A basic calculator that can perform arithmetic operations",
  "command": ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"],
  "type": "remote"
}
```

This ensures proper signal handling and more reliable startup in container environments. 