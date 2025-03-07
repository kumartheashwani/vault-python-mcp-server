@echo off
REM Script to build and run the Smithery container in stdio mode

echo Building Smithery container...
docker build -t mcp-calculator-smithery -f Dockerfile.smithery .

echo Running Smithery container in stdio mode...
docker run -i mcp-calculator-smithery 