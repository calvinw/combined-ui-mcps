#!/usr/bin/env python3
"""Example unified server that composes MCP services with proper lifespan management"""

from starlette.applications import Starlette
from starlette.routing import Mount
import uvicorn

# Import the MCP instances directly from individual services
from add_service import mcp as add_mcp
from greet_service import mcp as greet_mcp
from lifespan import combine_lifespans

# Create HTTP apps from each MCP server
add_app = add_mcp.http_app(transport="sse", path='/sse')
greet_app = greet_mcp.http_app(transport="sse", path='/sse')

# Create a Starlette app and mount the MCP servers at different routes
app = Starlette(
    routes=[
        Mount('/add/', app=add_app),
        Mount('/greet/', app=greet_app),
        # Add other routes as needed
    ],
    debug=True,
    lifespan=combine_lifespans(add_app.lifespan, greet_app.lifespan)
)

if __name__ == "__main__":
    print("Unified Service - MCP endpoints:")
    print("  Add Service: http://localhost:8000/add/sse")
    print("  Greet Service: http://localhost:8000/greet/sse")
    uvicorn.run(app, host='0.0.0.0', port=8000)
