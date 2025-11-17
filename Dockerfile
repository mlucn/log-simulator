# Multi-stage Dockerfile for Log Simulator API
# This creates a lightweight production image

# Stage 1: Build stage (not needed for now, but prepared for future frontend builds)
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better caching
COPY pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Stage 2: Runtime stage
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user for security
RUN groupadd -r logsim && useradd -r -g logsim logsim

# Set working directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY --chown=logsim:logsim . /app/

# Install Python dependencies
RUN pip install --no-cache-dir -e ".[api]"

# Create data directory for persistence
RUN mkdir -p /app/data && chown -R logsim:logsim /app/data

# Switch to non-root user
USER logsim

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/api/v1/health || exit 1

# Run the application
CMD ["uvicorn", "log_simulator.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
