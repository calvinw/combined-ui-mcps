from fastmcp import FastMCP
from fastapi import FastAPI

import sys
import os
import importlib.util

# Import add-service MCP
add_service_path = os.path.join(os.path.dirname(__file__), 'add-service', 'server.py')
add_spec = importlib.util.spec_from_file_location("add_server", add_service_path)
add_module = importlib.util.module_from_spec(add_spec)
add_spec.loader.exec_module(add_module)
add_mcp = add_module.mcp

# Import greet-service MCP
greet_service_path = os.path.join(os.path.dirname(__file__), 'greet-service', 'server.py')
greet_spec = importlib.util.spec_from_file_location("greet_server", greet_service_path)
greet_module = importlib.util.module_from_spec(greet_spec)
greet_spec.loader.exec_module(greet_module)
greet_mcp = greet_module.mcp

import contextlib

def combine_lifespans(*lifespans):
    """
    Combine multiple lifespan context managers into one.
    This allows for managing multiple session managers in a single lifespan context.
    Args:
        *lifespans: A variable number of lifespan context managers to combine.
    Returns:
        A combined lifespan context manager that yields control to the application.
    """
    @contextlib.asynccontextmanager
    async def combined_lifespan(app):
        async with contextlib.AsyncExitStack() as stack:
            for lifespan in lifespans:
                await stack.enter_async_context(lifespan(app))
            yield

    return combined_lifespan


# Create your FastMCP server as well as any tools, resources, etc.
mcp = FastMCP("MyServer")

# Create the ASGI app
add_app = add_mcp.http_app(transport="sse", path='/sse')
greet_app = greet_mcp.http_app(transport="sse", path='/sse')

# Create a FastAPI app and mount the MCP server
app = FastAPI(lifespan=combine_lifespans(greet_app.lifespan, add_app.lifespan))

app.mount("/add", add_app)
app.mount("/greet", greet_app)

def main():
    """Entry point for the combined-mcps CLI command"""
    import uvicorn
    print("🚀 Starting Combined MCP Server...")
    print("📍 Add Service: http://localhost:8000/add/sse")
    print("📍 Greet Service: http://localhost:8000/greet/sse")
    uvicorn.run("combined:app", port=8000, reload=True)

if __name__ == "__main__":
    main()
