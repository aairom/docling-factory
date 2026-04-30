# 🏭 Docling Factory - RAG Edition

A powerful, production-ready document parsing and RAG (Retrieval-Augmented Generation) application built with [Docling](https://github.com/docling-project/docling), [OpenSearch](https://opensearch.org/), [Ollama](https://ollama.ai/), and [LiteLLM](https://github.com/BerriAI/litellm). Parse documents and **chat with them** using local or remote LLMs.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Docling](https://img.shields.io/badge/docling-2.0+-purple.svg)
![OpenSearch](https://img.shields.io/badge/opensearch-2.0+-blue.svg)
![Ollama](https://img.shields.io/badge/ollama-local-green.svg)

## 📚 Documentation

- **[Getting Started](docs/GETTING_STARTED.md)** - Quick setup and first steps
- **[Comprehensive Guide](docs/COMPREHENSIVE_GUIDE.md)** - Complete documentation
- **[Architecture](docs/ARCHITECTURE.md)** - System design and workflows
- **[LiteLLM Integration](docs/LITELLM_INTEGRATION.md)** - ⭐ NEW: Remote LLM access guide
- **[Visual Dashboard](docs/VISUAL_DASHBOARD.md)** - Interactive metrics visualization
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[Python Compatibility](docs/PYTHON_COMPATIBILITY.md)** - Python version requirements

## ✨ Features

### 🤖 RAG & AI Features ⭐ NEW

- 💬 **Chat with Documents**
  - Ask questions about your parsed documents
  - Powered by local Ollama LLMs
  - Semantic search with OpenSearch vector database
  - Context-aware responses with source citations
  
- 🧠 **Flexible LLM Support**
  - **Local**: Use Ollama models (llama3.2, gemma3, granite, etc.)
  - **Remote**: Access 100+ LLMs via LiteLLM AI Gateway ⭐ NEW
    - OpenAI (GPT-4, GPT-3.5)
    - Anthropic (Claude)
    - Azure OpenAI
    - Google Vertex AI
    - AWS Bedrock
    - And many more!
  - Choose from multiple embedding models
  - Adjustable temperature and context settings
  - Easy switching between local and remote LLMs
  
- 🔍 **Semantic Search**
  - Vector-based document retrieval
  - OpenSearch with k-NN search
  - Configurable top-k results
  - Relevance scoring
  
- 📊 **OpenLLMetry Observability** ⭐ NEW
  - **Visual Dashboard** with interactive Plotly charts
    - Quality & Errors: finish reasons, error breakdown, rate limits
    - Token Usage & Cost: input/output tokens, cost tracking, throughput
    - Latency: P50/P95/P99 percentiles, time to first token, model comparison
    - Health Overview: request rate, error rate, active models
  - Real-time metrics with comprehensive statistics
  - Track all LLM interactions and operations
  - Performance metrics: latency (min/avg/p50/p95/p99/max), token usage
  - Request/response logging with detailed traces
  - Error tracking and debugging with error rates
  - Hourly activity monitoring
  - Model usage statistics
  - OpenTelemetry integration with custom metrics collector

### 📄 Document Processing Features

- 🎯 **Dual Processing Modes**
  - Individual file upload and processing
  - Batch processing of entire directories
  - Automatic RAG indexing option
  
- ⚡ **GPU Acceleration**
  - Optional GPU support for faster processing
  - Automatic fallback to CPU mode
  
- 📊 **Multiple Output Formats**
  - **Markdown** (.md) - Human-readable content
  - **HTML** (.html) - Web-ready format
  - **JSON** (.json) - Structured data for integration
  - **DocTags** (.txt) - Document structure tags
  - Select any combination of formats with checkboxes
  
- 🖼️ **Figure Extraction**
  - Extract images and figures from documents
  - Save figures separately with captions
  - Organized in dedicated subdirectories
  
- 🌈 **Multimodal Export**
  - Embed images directly in Markdown output
  - Base64-encoded images for self-contained documents
  - Perfect for rich document representation
  
- 🔍 **OCR Support**
  - **EasyOCR** - Deep learning-based OCR for multilingual documents
  - **Tesseract OCR** - Traditional OCR engine
  - **macOS Vision OCR** - Native macOS OCR (macOS only)
  - Force full page OCR option for scanned documents
  
- 📋 **XBRL Document Conversion**
  - Parse XBRL financial documents
  - Extract structured financial data
  - Convert to Markdown, HTML, or JSON
  
- 📊 **CSV File Conversion**
  - Convert CSV files to formatted tables
  - Output as Markdown tables, HTML tables, or JSON
  - Preserve data structure and formatting
  
- 🕐 **Timestamped Outputs**
  - All outputs are timestamped to prevent overwrites
  - Easy tracking of processing history
  
- 📈 **Real-time Progress Tracking**
  - Live progress updates during processing
  - Detailed status messages for each step
  - Progress bar for batch operations
  
- 🎨 **Modern Web Interface**
  - Clean, intuitive Gradio UI
  - Real-time processing feedback
  - Output management tools
  - Advanced feature controls
  
- 🔧 **Enhanced Parsing**
  - Powered by **Docling** and **Docling-Parse**
  - Advanced document structure recognition
  - Improved table and layout detection

## 📋 Supported Formats

### Input Formats
- PDF (`.pdf`) - with optional OCR
- Microsoft Word (`.docx`, `.doc`)
- Microsoft PowerPoint (`.pptx`)
- Microsoft Excel (`.xlsx`)
- HTML (`.html`)
- Markdown (`.md`)
- Plain Text (`.txt`)
- CSV (`.csv`) ⭐ NEW
- XBRL (`.xbrl`, `.xml`) ⭐ NEW

### Output Formats
- Markdown (`.md`) - with optional embedded images
- HTML (`.html`)
- JSON (`.json`)
- DocTags (`.txt`) - Document structure tags ⭐ NEW
- Extracted Figures (`.png`) ⭐ NEW

## 🚀 Quick Start

> **⚠️ IMPORTANT**: Always use `./scripts/launch.sh` or activate the virtual environment first!
>
> See **[Getting Started Guide](docs/GETTING_STARTED.md)** for detailed setup instructions.

### 3-Step Setup

```bash
# 1. Run setup (creates venv and installs dependencies)
./scripts/setup.sh

# 2. Start the application
./scripts/launch.sh

# 3. Open browser
# Navigate to http://localhost:7860
```

### Optional: RAG Features

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2:latest
ollama pull granite-embedding:30m

# Start OpenSearch
podman-compose -f docker-compose-opensearch.yml up -d

# Launch and initialize RAG in the UI
./scripts/launch.sh
```

## 📖 Usage

### Basic Workflow

1. **Configure Settings** - Select output formats, OCR engine, features
2. **Upload Documents** - Individual files or batch processing
3. **Parse** - Click "Parse Document" or "Process Batch"
4. **View Results** - Check output tabs or `output/` directory

### Key Features

- **Multiple Output Formats**: Markdown, HTML, JSON, DocTags
- **Figure Extraction**: Save images separately
- **Multimodal Export**: Embed images in Markdown
- **OCR Support**: RapidOCR, EasyOCR, Tesseract, macOS Vision
- **RAG Chat**: Ask questions about your documents
- **Batch Processing**: Process entire directories

For detailed usage instructions, see the [Comprehensive Guide](docs/COMPREHENSIVE_GUIDE.md).

## 🛠️ Scripts

```bash
./scripts/setup.sh [--gpu]              # Setup environment
./scripts/launch.sh [options]           # Start application
./scripts/stop.sh [--force]             # Stop application
./scripts/status.sh                     # Check status
./scripts/test.sh                       # Run tests
```

See [Getting Started](docs/GETTING_STARTED.md) for detailed script usage.

## 📁 Project Structure

```
docling-factory/
├── app.py                 # Main Gradio application
├── docling_parser.py      # Core parsing module
├── requirements.txt       # CPU dependencies
├── requirements-gpu.txt   # GPU dependencies
├── Dockerfile             # Docker image for CPU
├── Dockerfile.gpu         # Docker image for GPU
├── docker-compose.yml     # Docker Compose configuration
├── README.md              # This file
├── docs/                  # Documentation
│   ├── README.md          # Detailed documentation
│   ├── QUICKSTART.md      # Quick start guide
│   └── workflows.md       # Workflow diagrams
├── scripts/               # Automation scripts
│   ├── setup.sh           # Environment setup
│   ├── launch.sh          # Start application
│   ├── stop.sh            # Stop application
│   ├── status.sh          # Check status
│   ├── test.sh            # Run tests
│   └── github-push.sh     # Git initialization and push
├── k8s/                   # Kubernetes manifests
│   ├── namespace.yaml     # Namespace definition
│   ├── configmap.yaml     # Configuration
│   ├── pvc.yaml           # Persistent volumes
│   ├── deployment-cpu.yaml # CPU deployment
│   ├── deployment-gpu.yaml # GPU deployment
│   ├── service.yaml       # Services
│   ├── ingress.yaml       # Ingress configuration
│   ├── hpa.yaml           # Horizontal Pod Autoscaler
│   └── README.md          # Kubernetes deployment guide
├── input/                 # Input documents directory
├── output/                # Parsed outputs directory
└── logs/                  # Application logs
```

## 🔧 Configuration

### Environment Variables

```bash
export DOCLING_PORT=8080           # Custom port
export DOCLING_USE_GPU=true        # Enable GPU
export DOCLING_SHARE=true          # Create public link
export DOCLING_INPUT_DIR=./input   # Custom input directory
export DOCLING_OUTPUT_DIR=./output # Custom output directory
```

### Application Settings

Edit `app.py` to customize:
- Default port (line 318)
- Share settings (line 317)
- UI theme (line 182)

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Import errors | `./scripts/setup.sh` |
| Port in use | `./scripts/launch.sh --port 8080` |
| App won't stop | `./scripts/stop.sh --force` |
| GPU not detected | `python -c "import torch; print(torch.cuda.is_available())"` |

See [Troubleshooting Guide](docs/TROUBLESHOOTING.md) for detailed solutions.

## 🎯 Examples

```bash
# Parse single PDF with multiple formats
# 1. Upload PDF in UI
# 2. Select Markdown, HTML, JSON
# 3. Click "Parse Document"

# Batch process directory
# 1. Place PDFs in input/
# 2. Configure settings
# 3. Click "Process Batch"

# Use GPU acceleration
./scripts/launch.sh --gpu

# Chat with documents
# 1. Initialize RAG engine
# 2. Parse with "Index for RAG" enabled
# 3. Ask questions in Chat tab
```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# CPU version
docker-compose up docling-factory-cpu

# GPU version (requires nvidia-docker)
docker-compose --profile gpu up docling-factory-gpu
```

### Building Docker Images

```bash
# Build CPU image
docker build -t docling-factory:cpu -f Dockerfile .

# Build GPU image
docker build -t docling-factory:gpu -f Dockerfile.gpu .
```

### Running Docker Containers

```bash
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

## ☸️ Kubernetes Deployment

Deploy to Kubernetes for production-scale document processing:

```bash
# Deploy CPU version
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n docling-factory

# Access via port-forward
kubectl port-forward -n docling-factory svc/docling-factory 7860:80
```

For detailed Kubernetes deployment instructions, see [k8s/README.md](k8s/README.md).

## 🔍 API Usage

```python
from docling_parser import DoclingParser
from rag_engine import RAGEngine

# Parse documents
parser = DoclingParser(use_gpu=False)
result = parser.parse_document(
    "document.pdf",
    output_formats=['markdown', 'html'],
    export_figures=True,
    ocr_engine='rapidocr'
)

# RAG chat
rag = RAGEngine(
    embedding_model="granite-embedding:30m",
    llm_model="llama3.2:latest"
)
response = rag.chat("What is this document about?")
```

See [Comprehensive Guide](docs/COMPREHENSIVE_GUIDE.md) for complete API reference.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project uses the Docling library. Please refer to the [Docling license](https://github.com/docling-project/docling) for terms and conditions.

## 🔗 Links

### Document Processing
- [Docling Documentation](https://docling-project.github.io/docling/)
- [Docling GitHub](https://github.com/docling-project/docling)
- [Docling-Parse GitHub](https://github.com/docling-project/docling-parse)
- [Gradio Documentation](https://www.gradio.app/docs/)

### RAG & AI
- [OpenSearch Documentation](https://opensearch.org/docs/latest/)
- [OpenSearch GitHub](https://github.com/opensearch-project/OpenSearch)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Ollama Models](https://ollama.ai/library)
- [OpenLLMetry GitHub](https://github.com/traceloop/openllmetry)
- [LangChain Documentation](https://python.langchain.com/)

## 📞 Support

For issues related to:
- **This application**: Open an issue in this repository
- **Docling library**: Visit [Docling GitHub](https://github.com/docling-project/docling)
- **OpenSearch**: Visit [OpenSearch Forum](https://forum.opensearch.org/)
- **Ollama**: Visit [Ollama GitHub](https://github.com/ollama/ollama/issues)

## 🙏 Acknowledgments

- [Docling](https://github.com/docling-project/docling) - The powerful document parsing library
- [Docling-Parse](https://github.com/docling-project/docling-parse) - Enhanced parsing capabilities
- [OpenSearch](https://opensearch.org/) - Open source search and analytics engine
- [Ollama](https://ollama.ai/) - Run large language models locally
- [OpenLLMetry](https://github.com/traceloop/openllmetry) - LLM observability platform
- [LangChain](https://www.langchain.com/) - Framework for developing LLM applications
- [Gradio](https://www.gradio.app/) - The amazing UI framework

---

**Docling Factory** - Made with ❤️ for production-scale document processing