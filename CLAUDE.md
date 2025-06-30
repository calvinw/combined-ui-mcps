# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a combined MCP (Model Context Protocol) tool server built with FastMCP and FastAPI. The project demonstrates how to compose multiple MCP services into a unified server with proper lifespan management.

## Architecture

The project uses a modular architecture where individual MCP services are combined into a unified server:

- **Individual Services**: Each service (add_service.py, greet_service.py) is a standalone FastMCP server that can run independently
- **Combined Service**: The main combined_service.py composes multiple MCP services under different route mounts
- **Lifespan Management**: The lifespan.py module provides utilities to combine multiple lifespan context managers

### Key Components

- `combined_service.py`: Main entry point that mounts individual MCP services at different routes (/add/, /greet/)
- `add_service.py` & `greet_service.py`: Individual MCP services with their own tools
- `lifespan.py`: Utility for combining multiple lifespan context managers
- `pyproject.toml`: Project configuration with dependencies on fastapi, uvicorn, and fastmcp

## Development Commands

### Running the Combined Server
```bash
python combined_service.py
```
This starts the unified server on port 8000 with endpoints:
- Add Service: http://localhost:8000/add/sse
- Greet Service: http://localhost:8000/greet/sse

### Running Individual Services
Individual services can run standalone on different ports:
```bash
python add_service.py sse      # HTTP/SSE mode on port 8001
python add_service.py stdio    # MCP stdio mode
python greet_service.py sse    # HTTP/SSE mode on port 8001
python greet_service.py stdio  # MCP stdio mode
```

### Installation
```bash
pip install -e .
```

### Using the CLI Entry Point
After installation, you can run:
```bash
combined-mcps
```

## Service Architecture Patterns

When adding new MCP services:
1. Create a new service file following the pattern in add_service.py/greet_service.py
2. Import the MCP instance in combined_service.py
3. Mount the service at a new route using Mount('/newservice/', app=new_app)
4. Add the service's lifespan to the combine_lifespans call

Each service supports both stdio (for MCP clients) and SSE (for HTTP clients) transport modes.