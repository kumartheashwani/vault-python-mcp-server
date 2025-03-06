from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional, Union, Literal
import json

app = FastAPI()

class CalculatorTool:
    def __init__(self):
        self.name = "calculator"
        self.description = "A basic calculator that can perform arithmetic operations"
        self.parameters = {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The arithmetic operation to perform"
                },
                "numbers": {
                    "type": "array",
                    "items": {"type": "number"},
                    "description": "List of numbers to perform the operation on",
                    "minItems": 2
                }
            },
            "required": ["operation", "numbers"]
        }

    def execute(self, params: Dict[str, Any]) -> Any:
        operation = params["operation"]
        numbers = params["numbers"]

        if len(numbers) < 2:
            raise ValueError("At least two numbers are required")

        if operation == "add":
            return sum(numbers)
        elif operation == "subtract":
            return numbers[0] - sum(numbers[1:])
        elif operation == "multiply":
            result = 1
            for num in numbers:
                result *= num
            return result
        elif operation == "divide":
            if 0 in numbers[1:]:
                raise ValueError("Division by zero is not allowed")
            result = numbers[0]
            for num in numbers[1:]:
                result /= num
            return result
        else:
            raise ValueError(f"Unknown operation: {operation}")

# Initialize tools
calculator = CalculatorTool()
TOOLS = {
    calculator.name: calculator
}

class JsonRpcRequest(BaseModel):
    jsonrpc: Literal["2.0"]
    method: str
    params: Optional[Dict[str, Any]] = None
    id: Optional[Union[int, str]] = None

class JsonRpcResponse(BaseModel):
    jsonrpc: Literal["2.0"] = "2.0"
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[Union[int, str]] = None

class MCPServerState:
    def __init__(self):
        self.initialized = False
        self.client_info = None

server_state = MCPServerState()

# Standard REST endpoint for Smithery compatibility
@app.get("/tools")
async def get_tools():
    """Standard REST endpoint to list available tools"""
    tool_schemas = {}
    for name, tool in TOOLS.items():
        tool_schemas[name] = {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.parameters
        }
    return tool_schemas

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Helper function to process JSON-RPC requests
async def process_jsonrpc_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        request_model = JsonRpcRequest(**request_data)
    except Exception as e:
        return JsonRpcResponse(
            error={
                "code": -32700,
                "message": "Parse error",
                "data": str(e)
            },
            id=None
        ).dict()

    if request_model.method == "initialize" and not server_state.initialized:
        server_state.initialized = True
        server_state.client_info = request_model.params
        return JsonRpcResponse(
            result={
                "name": "Python MCP Calculator Server",
                "version": "1.0.0",
                "capabilities": {}
            },
            id=request_model.id
        ).dict()
    
    if not server_state.initialized:
        return JsonRpcResponse(
            error={
                "code": -32002,
                "message": "Server not initialized"
            },
            id=request_model.id
        ).dict()

    if request_model.method == "shutdown":
        server_state.initialized = False
        return JsonRpcResponse(result=None, id=request_model.id).dict()

    if request_model.method == "list_tools":
        tool_schemas = {}
        for name, tool in TOOLS.items():
            tool_schemas[name] = {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
        return JsonRpcResponse(result=tool_schemas, id=request_model.id).dict()

    if request_model.method == "execute":
        if not request_model.params or "function_calls" not in request_model.params:
            return JsonRpcResponse(
                error={
                    "code": -32602,
                    "message": "Invalid params: function_calls required"
                },
                id=request_model.id
            ).dict()

        results = []
        for call in request_model.params["function_calls"]:
            if call["name"] not in TOOLS:
                results.append({
                    "status": "error",
                    "error": f"Tool '{call['name']}' not found"
                })
                continue

            try:
                tool = TOOLS[call["name"]]
                result = tool.execute(call["parameters"])
                results.append({
                    "status": "success",
                    "result": result
                })
            except Exception as e:
                results.append({
                    "status": "error",
                    "error": str(e)
                })

        return JsonRpcResponse(result=results, id=request_model.id).dict()

    return JsonRpcResponse(
        error={
            "code": -32601,
            "message": f"Method '{request_model.method}' not found"
        },
        id=request_model.id
    ).dict()

@app.post("/")
async def handle_jsonrpc(request: Request):
    try:
        data = await request.json()
        return await process_jsonrpc_request(data)
    except Exception as e:
        return JsonRpcResponse(
            error={
                "code": -32700,
                "message": "Parse error",
                "data": str(e)
            },
            id=None
        ).dict()

# WebSocket endpoint for Smithery
@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            # Process the JSON-RPC request
            response = await process_jsonrpc_request(data)
            
            # Send response back to client
            await websocket.send_json(response)
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        # Send error response
        error_response = JsonRpcResponse(
            error={
                "code": -32603,
                "message": "Internal error",
                "data": str(e)
            },
            id=None
        ).dict()
        try:
            await websocket.send_json(error_response)
        except:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 