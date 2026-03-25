# Docling Factory - CPU Version
# Multi-stage build for optimized image size

FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy application files
COPY docling_parser.py .
COPY app_enhanced.py .
COPY rag_engine.py .
COPY metrics_collector.py .

# Create necessary directories
RUN mkdir -p input output output/figures logs

# Expose Gradio port
EXPOSE 7860

# Set environment variables
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860
ENV PYTHONUNBUFFERED=1
ENV OPENSEARCH_HOST=opensearch
ENV OPENSEARCH_PORT=9200
ENV OLLAMA_BASE_URL=http://host.docker.internal:11434

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:7860')" || exit 1

# Run the application
CMD ["python", "app_enhanced.py"]