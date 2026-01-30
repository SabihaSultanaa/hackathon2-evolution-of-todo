# Use Python slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies directly
RUN pip install --no-cache-dir \
    fastapi==0.115.6 \
    uvicorn==0.34.0 \
    openai==1.59.5 \
    python-dotenv==1.0.1 \
    pydantic==2.10.5 \
    httpx==0.28.1

# Copy application code
COPY . /app/ai_agent

# Set Python path so ai_agent module can be found
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8001

# Start the server from the ai_agent directory
WORKDIR /app/ai_agent
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]