@echo off
REM Start script for container deployments
REM This script starts the server in HTTP mode for reliable API access

echo Starting MCP Calculator Server in HTTP mode for container deployment...

REM Ensure logs directory exists
if not exist logs mkdir logs

REM Set HTTP mode
set MCP_HTTP_MODE=1

REM Start the server in HTTP mode
python http_server.py 