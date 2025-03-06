# MCP Calculator Server

A Model Context Protocol (MCP) server implementation with a basic calculator tool. This server can be deployed in Smithery and provides arithmetic operations through a REST API.

## Features

- Basic arithmetic operations (add, subtract, multiply, divide)
- MCP-compliant API endpoints
- JSON schema validation
- Error handling

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

Start the server with:
```bash
python server.py
```

The server will run on `http://localhost:8000`

## API Endpoints

- `GET /`: Health check endpoint
- `GET /tools`: List available tools and their schemas
- `POST /execute`: Execute tool operations

## Using the Calculator Tool

Example request to the `/execute` endpoint:

```json
{
    "function_calls": [
        {
            "name": "calculator",
            "parameters": {
                "operation": "add",
                "numbers": [1, 2, 3, 4]
            }
        }
    ]
}
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

## Deployment in Smithery

This server is designed to be deployed in Smithery. Follow Smithery's documentation for deployment instructions. 