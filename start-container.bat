@echo off
REM Start script for container deployments
REM This script starts the server in HTTP mode for reliable API access

echo Starting MCP Calculator Server in HTTP mode for container deployment...
uvicorn server:app --host 0.0.0.0 --port 8000 