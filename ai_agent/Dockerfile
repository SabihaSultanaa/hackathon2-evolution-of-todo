FROM python:3.12-slim

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
ENV PYTHONPATH=/app

# Install requirements
RUN uv pip install --system psycopg2-binary openai fastapi uvicorn python-dotenv

# Copy the ai_agent code into a folder named ai_agent
COPY . /app/ai_agent/
RUN touch /app/ai_agent/__init__.py

# Start the FastAPI server
CMD ["uvicorn", "ai_agent.main:app", "--host", "0.0.0.0", "--port", "8001"]