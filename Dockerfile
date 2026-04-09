# Dockerfile for Hello World FastAPI application
FROM python:3.12-slim

LABEL maintainer="team" \
      description="Minimal Hello World FastAPI service"

WORKDIR /app

# Install dependencies first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY tests/ tests/
COPY conftest.py .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
