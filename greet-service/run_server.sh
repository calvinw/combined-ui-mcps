#!/bin/bash
set -e

echo "🚀 Starting Greet Service SSE server..."

# Sync dependencies
uv sync

# Start SSE server
echo "🔧 Starting Greet Service SSE server on port 8001..."
uv run python server.py sse
