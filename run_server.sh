#!/bin/bash
set -e

echo "🚀 Starting Combined MCP Server..."

# Sync dependencies
uv sync

# Start combined server
echo "🔧 Starting Combined MCP Server on port 8000..."
echo "📍 Add Service: http://localhost:8000/add/sse"
echo "📍 Greet Service: http://localhost:8000/greet/sse"
uv run python combined.py
