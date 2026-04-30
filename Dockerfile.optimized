# Docling Factory - CPU Version (Optimized Build)
# Multi-stage build with better caching and faster builds

FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better caching
COPY requirements.txt .

# Install dependencies in stages for better caching
# Stage 1: Install lightweight dependencies first
RUN pip install --no-cache-dir --user \
    numpy>=1.24.0,<2.0.0 \
    pandas>=2.0.0 \
    pillow>=10.0.0 \
    python-docx>=1.1.0 \
    PyPDF2>=3.0.0 \
    python-dateutil>=2.8.2 \
    pathlib>=1.0.1 \
    lxml>=4.9.0 \
    openpyxl>=3.1.0

# Stage 2: Install medium-weight dependencies
RUN pip install --no-cache-dir --user \
    gradio>=4.0.0 \
    streamlit>=1.31.0 \
    plotly>=5.18.0 \
    httpx>=0.24.0 \
    tiktoken>=0.5.0

# Stage 3: Install OpenSearch and LangChain
RUN pip install --no-cache-dir --user \
    opensearch-py>=2.4.0 \
    langchain>=0.1.0 \
    langchain-community>=0.0.20

# Stage 4: Install LLM clients (lightweight)
RUN pip install --no-cache-dir --user \
    ollama>=0.1.0 \
    litellm>=1.0.0

# Stage 5: Install OpenTelemetry (lightweight)
RUN pip install --no-cache-dir --user \
    opentelemetry-api>=1.20.0 \
    opentelemetry-sdk>=1.20.0 \
    opentelemetry-instrumentation>=0.41b0 \
    traceloop-sdk>=0.30.0

# Stage 6: Install Docling (can be slow)
RUN pip install --no-cache-dir --user \
    docling>=2.0.0 \
    docling-core>=2.0.0 \
    docling-parse>=2.0.0 \
    python-xbrl>=1.1.1

# Stage 7: Install CV dependencies (slowest - do last)
RUN pip install --no-cache-dir --user \
    opencv-python-headless>=4.8.0,<5.0.0 \
    scikit-image>=0.21.0 \
    pytesseract>=0.3.10

# Stage 8: Install PyTorch (very slow - separate for better error handling)
RUN pip install --no-cache-dir --user \
    torch>=2.0.0 \
    torchvision>=0.15.0 \
    || echo "PyTorch installation failed, continuing..."

# Stage 9: Install ML dependencies (slow)
RUN pip install --no-cache-dir --user \
    sentence-transformers>=2.2.0 \
    faiss-cpu>=1.7.4 \
    chromadb>=0.4.0 \
    || echo "ML dependencies installation failed, continuing..."

# Stage 10: Install EasyOCR last (slowest)
RUN pip install --no-cache-dir --user \
    easyocr>=1.7.0 \
    || echo "EasyOCR installation failed, continuing..."

# Final stage
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
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
COPY standalone_dashboard.py .
COPY metrics_dashboard.py .

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
ENV LITELLM_API_BASE=http://litellm:4000
ENV LITELLM_API_KEY=sk-1234

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:7860')" || exit 1

# Run the application
CMD ["python", "app_enhanced.py"]