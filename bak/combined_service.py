#!/usr/bin/env python3
"""Example unified server that composes MCP services with proper lifespan management"""

import os
import logging
from starlette.applications import Starlette
from starlette.routing import Mount
import uvicorn

# Configure logging based on quiet mode
quiet_mode = os.getenv('MCP_QUIET', '0') == '1'
if quiet_mode:
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn").setLevel(logging.WARNING)

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
    import os
    quiet_mode = os.getenv('MCP_QUIET', '0') == '1'
    
    if not quiet_mode:
        print("Unified Service - MCP endpoints:")
        print("  Add Service: http://localhost:8000/add/sse")
        print("  Greet Service: http://localhost:8000/greet/sse")
    
    # Configure logging level for uvicorn
    log_level = "warning" if quiet_mode else "info"
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level=log_level)
