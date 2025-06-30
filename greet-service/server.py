from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import HTMLResponse
import sys

mcp = FastMCP("GreetServer")


@mcp.tool
def greet_someone(name: str) -> str:
    """Greet someone by name"""
    return f"Hello, {name}!"


@mcp.custom_route("/greet_page", methods=["GET"])
async def greet_page(request: Request) -> HTMLResponse:
    return HTMLResponse("""
    <h1>Greet Service</h1>
    <p>MCP Endpoint: <code>/sse</code></p>
    <p>Tool: <code>greet_someone(name)</code> - Greet someone by name</p>
    """)

# Create the app instance at module level for uvicorn reload
app = mcp.http_app(transport="sse", path='/sse')

def main():
    """Entry point for the greet-service CLI command"""
    transport = sys.argv[1] if len(sys.argv) > 1 else "sse"
    
    if transport == "stdio":
        mcp.run()
    else:  # sse
        import uvicorn
        uvicorn.run("server:app", port=8001, reload=True)

if __name__ == "__main__":
    main()
