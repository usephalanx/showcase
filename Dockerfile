FROM python:3.12-slim

LABEL maintainer="dev-team"

WORKDIR /app

# Install dependencies first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY main.py .
COPY routes.py .
COPY models.py .
COPY storage.py .
COPY conftest.py .
COPY tests/ tests/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
