@echo off
REM Start script for Smithery integration as a local tool
REM This script starts the server in stdio mode for communication with Smithery

echo Starting MCP Calculator Server in stdio mode for Smithery local tool integration...

REM Ensure HTTP mode is not set
set MCP_HTTP_MODE=

REM Set stdio mode
set MCP_STDIO_MODE=1

REM Verify mode (optional)
if exist verify-mode.py (
    echo Verifying mode configuration...
    python verify-mode.py
    if errorlevel 1 (
        echo Mode verification failed. Please check the configuration.
        exit /b 1
    )
)

REM Start the server in stdio mode
python server.py 