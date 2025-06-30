FROM python:3.11-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Copy project files
COPY pyproject.toml ./
COPY server.py ./

# Install dependencies
RUN uv sync --frozen

# Expose port
EXPOSE 8001

# Start the server
CMD ["uv", "run", "python", "server.py", "sse"]