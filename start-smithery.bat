@echo off
REM Start script for Smithery integration as a local tool
REM This script starts the server in stdio mode for communication with Smithery

echo Starting MCP Calculator Server in stdio mode for Smithery local tool integration...
set MCP_STDIO_MODE=1
python server.py 