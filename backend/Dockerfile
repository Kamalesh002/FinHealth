# Backend Dockerfile for Railway
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Railway uses PORT env variable
ENV PORT=8000

# Expose port (optional, Railway handles this)
EXPOSE ${PORT}

# Run the application using shell form to expand $PORT
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}
