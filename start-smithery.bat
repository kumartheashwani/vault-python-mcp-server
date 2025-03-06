@echo off
REM Start script for Smithery integration
REM This script uses the adaptive mode selection:
REM - If stdin is available, it runs in stdio mode
REM - If stdin is not available, it falls back to HTTP mode

echo Starting MCP Calculator Server with adaptive mode selection...
python smithery_mode.py 