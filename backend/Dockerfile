FROM python:3.12-slim

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
ENV PYTHONPATH=/app

# Copy dependency files
COPY backend/pyproject.toml backend/uv.lock ./
RUN uv pip install --system -r pyproject.toml

# Copy both folders into the container correctly
COPY backend /app/app
COPY ai_agent /app/ai_agent

# Create the missing __init__ file just in case
RUN touch /app/ai_agent/__init__.py

# Start the server
CMD ["python", "-c", "import time; while True: time.sleep(3600)"]