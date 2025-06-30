FROM python:3.11-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Copy project files
COPY pyproject.toml uv.lock ./
COPY combined.py ./

# Copy service directories
COPY add-service/server.py ./add-service/
COPY greet-service/server.py ./greet-service/

# Install dependencies
RUN uv sync --frozen

# Expose port
EXPOSE 8000

# Start the combined server
CMD ["uv", "run", "python", "combined.py"]