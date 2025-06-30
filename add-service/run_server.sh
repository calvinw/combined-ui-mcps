#!/bin/bash
set -e

echo "🚀 Starting Add Service SSE server..."

# Sync dependencies
uv sync

# Start SSE server
echo "🔧 Starting Add Service SSE server on port 8001..."
uv run python server.py sse
