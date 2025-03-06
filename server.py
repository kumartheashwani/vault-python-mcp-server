from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
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

class FunctionCall(BaseModel):
    name: str
    parameters: Dict[str, Any]

class MCPRequest(BaseModel):
    function_calls: List[FunctionCall]

@app.get("/")
async def root():
    return {"message": "MCP Calculator Server is running"}

@app.get("/tools")
async def list_tools():
    tool_schemas = {}
    for name, tool in TOOLS.items():
        tool_schemas[name] = {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.parameters
        }
    return tool_schemas

@app.post("/execute")
async def execute_tools(request: MCPRequest):
    results = []
    
    for call in request.function_calls:
        if call.name not in TOOLS:
            raise HTTPException(status_code=404, detail=f"Tool '{call.name}' not found")
        
        try:
            tool = TOOLS[call.name]
            result = tool.execute(call.parameters)
            results.append({
                "status": "success",
                "result": result
            })
        except Exception as e:
            results.append({
                "status": "error",
                "error": str(e)
            })
    
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 