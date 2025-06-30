from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import HTMLResponse
import sys

mcp = FastMCP("AddServer")

@mcp.tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

@mcp.custom_route("/add_page", methods=["GET"])
async def add_page(request: Request) -> HTMLResponse:
    return HTMLResponse("""
    <h1>Add Numbers Service</h1>
    <p>MCP Endpoint: <code>/sse</code></p>
    <p>Tool: <code>add_numbers(a, b)</code> - Add two numbers together</p>
    """)

# Create the app instance at module level for uvicorn reload
app = mcp.http_app(transport="sse", path='/sse')

def main():
    """Entry point for the add-service CLI command"""
    transport = sys.argv[1] if len(sys.argv) > 1 else "sse"
    
    if transport == "stdio":
        mcp.run()
    else:  # sse
        import uvicorn
        uvicorn.run("server:app", port=8001, reload=True)

if __name__ == "__main__":
    main()
