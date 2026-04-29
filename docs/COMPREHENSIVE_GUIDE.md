# Docling Factory - Comprehensive Guide

Complete documentation for the Docling Factory RAG Edition.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [RAG System](#rag-system)
- [API Reference](#api-reference)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

---

## Overview

**Docling Factory** is a production-ready document parsing and RAG (Retrieval-Augmented Generation) application built with:
- [Docling](https://github.com/docling-project/docling) - Document parsing
- [OpenSearch](https://opensearch.org/) - Vector database
- [Ollama](https://ollama.ai/) - Local LLM runtime
- [Gradio](https://www.gradio.app/) - Web interface

### Supported Input Formats

- PDF (`.pdf`) - with OCR support
- Microsoft Word (`.docx`, `.doc`)
- Microsoft PowerPoint (`.pptx`)
- Microsoft Excel (`.xlsx`)
- HTML (`.html`)
- Markdown (`.md`)
- Plain Text (`.txt`)
- CSV (`.csv`)
- XBRL (`.xbrl`, `.xml`)

### Output Formats

- Markdown (`.md`) - with optional embedded images
- HTML (`.html`)
- JSON (`.json`)
- DocTags (`.txt`) - Document structure tags
- Extracted Figures (`.png`)

---

## Features

### Document Processing

- **Dual Processing Modes**: Individual upload or batch processing
- **GPU Acceleration**: Optional CUDA support for faster processing
- **Multiple Output Formats**: Selectable via checkboxes
- **Figure Extraction**: Save images and diagrams separately
- **Multimodal Export**: Embed images directly in Markdown
- **OCR Support**: RapidOCR, EasyOCR, Tesseract, macOS Vision
- **CSV/XBRL Conversion**: Convert to formatted tables
- **Timestamped Outputs**: Prevent overwrites
- **Real-time Progress**: Live updates during processing

### RAG & AI Features

- **Chat with Documents**: Ask questions about parsed documents
- **Local LLM Support**: Use Ollama models (llama3.2, gemma3, granite, etc.)
- **Semantic Search**: Vector-based retrieval with OpenSearch
- **Context-Aware Responses**: With source citations
- **OpenLLMetry Observability**: Real-time metrics and tracing
- **Multiple Embedding Models**: Choose from various options

---

## Installation

### Prerequisites

- Python 3.8+
- pip package manager
- Podman or Docker (for OpenSearch)
- Ollama (for LLM features)
- (Optional) CUDA-compatible GPU

### Basic Installation

```bash
# Navigate to project directory
cd docling-factory

# Run setup script
./scripts/setup.sh

# For GPU support
./scripts/setup.sh --gpu
```

### Manual Installation

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# For GPU support
pip install -r requirements-gpu.txt
```

### Ollama Setup

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull LLM models
ollama pull llama3.2:latest
ollama pull gemma3:4b
ollama pull ibm/granite4:3b

# Pull embedding models
ollama pull granite-embedding:30m
ollama pull embeddinggemma:latest
```

### OpenSearch Setup

```bash
# Using Podman
podman-compose -f docker-compose-opensearch.yml up -d

# Using Docker
docker-compose -f docker-compose-opensearch.yml up -d

# Verify
curl http://localhost:9200
```

---

## Configuration

### Environment Variables

```bash
# Application Settings
export DOCLING_PORT=7860
export DOCLING_USE_GPU=false
export DOCLING_SHARE=false
export DOCLING_INPUT_DIR=./input
export DOCLING_OUTPUT_DIR=./output

# OpenSearch Settings
export OPENSEARCH_HOST=localhost
export OPENSEARCH_PORT=9200
export OPENSEARCH_USER=admin
export OPENSEARCH_PASSWORD=admin

# Ollama Settings
export OLLAMA_BASE_URL=http://localhost:11434

# OpenLLMetry Settings (optional)
export TRACELOOP_API_KEY=your_key_here
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
```

### Application Settings

Edit `app_enhanced.py` to customize:
- Default port (line 318)
- Share settings (line 317)
- UI theme (line 182)

---

## Usage

### Starting the Application

```bash
# Standard launch
./scripts/launch.sh

# With options
./scripts/launch.sh --detached --port 8080 --gpu --share

# Manual launch
source venv/bin/activate
python app_enhanced.py
```

### Individual File Processing

1. Open http://localhost:7860
2. **Configure Global Settings:**
   - Select output formats (Markdown, HTML, JSON, DocTags)
   - Enable Extract Figures
   - Enable Multimodal Export
   - Select OCR engine
   - Enable Force Full Page OCR (for scanned docs)
3. Go to **"📤 Individual Upload"** tab
4. Upload document(s)
5. Click **"🚀 Parse Document"**
6. View results in format tabs

### Batch Processing

1. Place documents in `input/` directory
2. Configure settings
3. Go to **"📦 Batch Processing"** tab
4. Click **"🚀 Process Batch"**
5. Monitor progress bar
6. Check `output/` directory for results

### Output Management

1. Go to **"📁 Output Management"** tab
2. Click **"🔄 Refresh File List"**
3. Set days threshold
4. Click **"🗑️ Clear Outputs"** to clean old files

---

## RAG System

### Initialization

1. Start OpenSearch and Ollama
2. Launch application
3. Go to **"💬 Chat with Documents"** tab
4. Select models:
   - **LLM Model**: llama3.2:latest (or your choice)
   - **Embedding Model**: granite-embedding:30m
5. Enable OpenLLMetry Tracing
6. Click **"🔧 Initialize RAG Engine"**

### Indexing Documents

**Option A: Parse and Index**
1. Go to **"📤 Upload & Parse"** tab
2. Enable **"Index for RAG"** checkbox
3. Upload and parse document
4. Document automatically indexed

**Option B: Programmatic Indexing**
```python
from rag_engine import RAGEngine

rag = RAGEngine(
    embedding_model="granite-embedding:30m",
    llm_model="llama3.2:latest"
)

# Index document
with open("output/document.md", "r") as f:
    content = f.read()
    
result = rag.index_document(
    file_path="document.pdf",
    content=content,
    metadata={"source": "upload"}
)
```

### Chatting with Documents

1. Go to **"💬 Chat with Documents"** tab
2. Adjust settings:
   - **Temperature**: 0.0 (precise) to 1.0 (creative)
   - **Context Chunks**: 1-10 (default: 5)
3. Type question
4. Click **"📤 Send"** or press Enter

### Monitoring

**RAG Statistics Tab:**
- Total indexed chunks
- Number of unique documents
- Index size
- System health status

**OpenLLMetry Tab:**
- Real-time metrics dashboard
- LLM call tracing
- Performance metrics (latency, tokens)
- Error tracking
- Hourly activity monitoring

---

## API Reference

### DoclingParser Class

```python
from docling_parser import DoclingParser

# Initialize
parser = DoclingParser(use_gpu=False, output_dir="output")

# Parse single document
result = parser.parse_document(
    "document.pdf",
    output_formats=['markdown', 'html', 'json'],
    export_figures=True,
    export_multimodal=False,
    ocr_engine='rapidocr',
    force_ocr=False
)

# Parse batch
results = parser.parse_batch(
    "input",
    output_formats=['markdown', 'json'],
    export_figures=True,
    ocr_engine='easyocr',
    force_ocr=True
)

# Get available OCR engines
ocr_engines = parser.get_ocr_engines()

# Get supported formats
formats = parser.get_supported_formats()

# Clear old outputs
parser.clear_output_directory(older_than_days=7)
```

### RAGEngine Class

```python
from rag_engine import RAGEngine

# Initialize
rag = RAGEngine(
    opensearch_host="localhost",
    opensearch_port=9200,
    ollama_base_url="http://localhost:11434",
    embedding_model="granite-embedding:30m",
    llm_model="llama3.2:latest",
    index_name="documents",
    enable_tracing=True
)

# Index document
result = rag.index_document(
    file_path="document.pdf",
    content="Document content...",
    metadata={"source": "upload"}
)

# Search
results = rag.search("machine learning", top_k=5)

# Chat
response = rag.chat(
    query="Explain the concept",
    top_k=3,
    temperature=0.3
)

# Get statistics
stats = rag.get_stats()
health = rag.health_check()

# List documents
docs = rag.list_indexed_documents()

# Delete document
result = rag.delete_document("document.pdf")
```

---

## Deployment

### Docker Deployment

```bash
# Build CPU image
docker build -t docling-factory:cpu -f Dockerfile .

# Build GPU image
docker build -t docling-factory:gpu -f Dockerfile.gpu .

# Run CPU version
docker run -p 7860:7860 \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  docling-factory:cpu

# Run GPU version
docker run --gpus all -p 7860:7860 \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  docling-factory:gpu
```

### Docker Compose

```bash
# CPU version
docker-compose up docling-factory-cpu

# GPU version (requires nvidia-docker)
docker-compose --profile gpu up docling-factory-gpu
```

### Kubernetes Deployment

```bash
# Deploy CPU version
kubectl apply -f k8s/

# Check deployment
kubectl get pods -n docling-factory

# Access via port-forward
kubectl port-forward -n docling-factory svc/docling-factory 7860:80
```

See [`k8s/README.md`](../k8s/README.md) for detailed Kubernetes instructions.

---

## Troubleshooting

### EasyOCR "Not Installed" Error

**Problem**: Error appears even though EasyOCR is installed.

**Solution**: Always activate virtual environment:
```bash
./scripts/launch.sh
# OR
source venv/bin/activate && python app_enhanced.py
```

### OpenSearch Connection Issues

**Problem**: Cannot connect to OpenSearch.

**Solutions**:
```bash
# Verify OpenSearch is running
podman ps | grep opensearch

# Check health
curl http://localhost:9200/_cluster/health

# Restart
podman-compose -f docker-compose-opensearch.yml restart
```

### Ollama Model Not Found

**Problem**: Selected model not available.

**Solutions**:
```bash
# List models
ollama list

# Pull missing model
ollama pull llama3.2:latest

# Verify Ollama
curl http://localhost:11434/api/tags
```

### Port Already in Use

**Problem**: Port 7860 already in use.

**Solutions**:
```bash
# Check what's using the port
lsof -i :7860

# Stop existing process
./scripts/stop.sh

# Use different port
./scripts/launch.sh --port 8080
```

### GPU Not Working

**Problem**: GPU acceleration not being used.

**Solutions**:
```bash
# Check GPU availability
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"

# Install GPU requirements
source venv/bin/activate
pip install -r requirements-gpu.txt

# Launch with GPU flag
./scripts/launch.sh --gpu
```

### Memory Issues

**Problem**: Out of memory errors.

**Solutions**:
1. Use smaller models (llama3.2:latest instead of larger models)
2. Reduce chunk size in `rag_engine.py`
3. Limit context chunks (lower top_k value)
4. Process fewer documents at once

### Slow Response Times

**Problem**: RAG responses are slow.

**Solutions**:
1. Use faster models (llama3.2:latest)
2. Reduce context chunks (lower top_k)
3. Enable GPU acceleration
4. Optimize OpenSearch settings

---

## Performance Optimization

### CPU vs GPU Mode

| Mode | Speed | Memory | Best For |
|------|-------|--------|----------|
| CPU | 1-2 pages/sec | 100-500 MB | Small batches, occasional use |
| GPU | 3-10 pages/sec | 500 MB - 2 GB | Large batches, frequent use |

### Model Selection

**LLM Models:**
| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| llama3.2:latest | 2GB | Fast | Good | General purpose |
| gemma3:4b | 3.3GB | Medium | High | Balanced performance |
| ibm/granite4:3b | 2.1GB | Fast | Good | Technical documents |

**Embedding Models:**
| Model | Size | Dimension | Speed |
|-------|------|-----------|-------|
| granite-embedding:30m | 62MB | 384 | Fast |
| embeddinggemma:latest | 621MB | 768 | Medium |

### Best Practices

1. **Document Preparation**
   - Use OCR for scanned documents
   - Extract figures for better context
   - Clean formatting before indexing

2. **Query Formulation**
   - Be specific in questions
   - Use keywords from documents
   - Ask one question at a time

3. **Monitoring**
   - Enable OpenLLMetry tracing
   - Monitor response times
   - Track token usage
   - Review error logs

---

## Support & Resources

### Documentation
- [Getting Started](GETTING_STARTED.md)
- [Architecture](ARCHITECTURE.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Workflows](workflows.md)

### External Links
- [Docling Documentation](https://docling-project.github.io/docling/)
- [OpenSearch Documentation](https://opensearch.org/docs/latest/)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Gradio Documentation](https://www.gradio.app/docs/)

### Getting Help
1. Check troubleshooting section
2. Review application logs: `tail -f logs/app.log`
3. Check system status: `./scripts/status.sh`
4. Open an issue on GitHub

---

**Made with ❤️ for production-scale document processing**