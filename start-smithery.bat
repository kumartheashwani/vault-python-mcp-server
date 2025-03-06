@echo off
REM Start script for Smithery integration
REM This script ensures the MCP server starts EXCLUSIVELY in stdio mode
REM without launching the HTTP server

echo Starting MCP Calculator Server in EXCLUSIVE stdio mode for Smithery...
python smithery_mode.py 