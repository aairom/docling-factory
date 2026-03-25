# 🏭 Docling Factory - RAG Edition

A powerful, production-ready document parsing and RAG (Retrieval-Augmented Generation) application built with [Docling](https://github.com/docling-project/docling), [OpenSearch](https://opensearch.org/), and [Ollama](https://ollama.ai/). Parse documents and **chat with them** using local LLMs with advanced features including **RAG**, **multimodal export**, **figure extraction**, **OCR support**, and **OpenLLMetry observability**.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Docling](https://img.shields.io/badge/docling-2.0+-purple.svg)
![OpenSearch](https://img.shields.io/badge/opensearch-2.0+-blue.svg)
![Ollama](https://img.shields.io/badge/ollama-local-green.svg)

## ✨ Features

### 🤖 RAG & AI Features ⭐ NEW

- 💬 **Chat with Documents**
  - Ask questions about your parsed documents
  - Powered by local Ollama LLMs
  - Semantic search with OpenSearch vector database
  - Context-aware responses with source citations
  
- 🧠 **Local LLM Support**
  - Use your own Ollama models (llama3.2, gemma3, granite, etc.)
  - No cloud dependencies - 100% local
  - Choose from multiple embedding models
  - Adjustable temperature and context settings
  
- 🔍 **Semantic Search**
  - Vector-based document retrieval
  - OpenSearch with k-NN search
  - Configurable top-k results
  - Relevance scoring
  
- 📊 **OpenLLMetry Observability** ⭐ NEW
  - Track all LLM interactions
  - Performance metrics and latency monitoring
  - Request/response logging
  - Error tracking and debugging
  - OpenTelemetry integration

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

### Prerequisites

- Python 3.8 or higher
- pip package manager
- **Podman or Docker** (for OpenSearch)
- **Ollama** (for local LLM)
- (Optional) CUDA-compatible GPU for GPU acceleration

### Installation

1. **Clone or download this repository**

```bash
cd docling-factory
```

2. **Install Ollama and pull models**

```bash
# Install Ollama (macOS/Linux)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull required models
ollama pull llama3.2:latest
ollama pull granite-embedding:30m
```

3. **Start OpenSearch (for RAG)**

```bash
# Using Podman
podman-compose -f docker-compose-opensearch.yml up -d

# Or using Docker
docker-compose -f docker-compose-opensearch.yml up -d
```

4. **Run the setup script**

```bash
# For CPU version (recommended for most users)
./scripts/setup.sh

# For GPU version (requires CUDA)
./scripts/setup.sh --gpu
```

5. **Start the application**

```bash
# Standard app
./scripts/launch.sh

# Or RAG-enabled app
source venv/bin/activate
python app_enhanced.py
```

6. **Open your browser**

Navigate to `http://localhost:7860`

### Quick RAG Setup

For detailed RAG setup instructions, see [RAG Setup Guide](docs/RAG_SETUP.md).

1. Start OpenSearch and Ollama (steps 2-3 above)
2. Launch `app_enhanced.py`
3. Go to "💬 Chat with Documents" tab
4. Click "🔧 Initialize RAG Engine"
5. Parse documents with "Index for RAG" enabled
6. Start chatting with your documents!

## 📖 Usage

### Individual File Processing

1. Open the web interface at `http://localhost:7860`
2. **Configure Global Settings:**
   - Enable GPU acceleration (optional)
   - **Select output formats**: Markdown, HTML, JSON, DocTags
   - **Enable advanced features**:
     - ✅ Extract Figures - Save images separately
     - ✅ Multimodal Export - Embed images in Markdown
   - **Configure OCR**:
     - Select OCR engine (EasyOCR, Tesseract, macOS Vision, or None)
     - Enable "Force Full Page OCR" for scanned documents
3. Navigate to the **"📤 Individual Upload"** tab
4. Click **"Upload Document"** and select your file
5. Click **"🚀 Parse Document"**
6. Watch the **real-time progress** updates
7. View results in separate tabs for each format

### Batch Processing

1. Place documents in the `input/` directory
2. Open the web interface
3. **Configure settings** (output formats, OCR, figure extraction, etc.)
4. Navigate to the **"📦 Batch Processing"** tab
5. Click **"🚀 Process Batch"**
6. Watch the **progress bar** and status updates
7. View processing summary with figure counts and OCR info
8. Check `output/` directory for results
   - Documents in selected formats
   - Figures in `output/figures/` subdirectories

### Advanced Features

#### Figure Extraction
Enable "Extract Figures" to save all images and figures separately:
- Figures saved in `output/figures/[document_name]/`
- Each figure saved as `figure_N.png`
- Captions saved as `figure_N_caption.txt`

#### Multimodal Export
Enable "Multimodal Export" to embed images directly in Markdown:
- Images encoded as base64
- Self-contained Markdown files
- Perfect for sharing or archiving

#### OCR Processing
Select an OCR engine for text extraction:
- **EasyOCR**: Best for multilingual documents, uses deep learning
- **Tesseract**: Traditional OCR, requires separate installation
- **macOS Vision**: Native macOS OCR (macOS only)
- **Force Full Page OCR**: Apply OCR even when text is extractable

#### CSV Conversion
Upload CSV files to convert them to:
- Markdown tables
- HTML tables
- JSON arrays

#### XBRL Processing
Upload XBRL financial documents to extract:
- Financial facts and data
- Structured information
- Convert to readable formats

### Output Management

1. Navigate to the **"📁 Output Management"** tab
2. Click **"🔄 Refresh File List"** to see all outputs
3. Set days threshold and click **"🗑️ Clear Outputs"** to clean old files

## 🛠️ Scripts

The `scripts/` directory contains automation scripts:

### Setup Script
```bash
./scripts/setup.sh          # Setup CPU version
./scripts/setup.sh --gpu    # Setup GPU version
```

### Launch Script
```bash
./scripts/launch.sh                    # Start in foreground
./scripts/launch.sh --detached         # Start in background
./scripts/launch.sh --port 8080        # Custom port
./scripts/launch.sh --gpu              # Enable GPU
./scripts/launch.sh -d -p 8080 --gpu   # Combined options
```

### Stop Script
```bash
./scripts/stop.sh          # Gracefully stop
./scripts/stop.sh --force  # Force stop
```

### Status Script
```bash
./scripts/status.sh        # Check application status
```

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

## 📚 Documentation

For detailed documentation, see:
- [Full Documentation](docs/README.md) - Complete guide with API reference
- [RAG Setup Guide](docs/RAG_SETUP.md) - Complete RAG setup and usage guide ⭐ NEW
- [Architecture](docs/ARCHITECTURE.md) - System architecture and design
- [Quick Start](docs/QUICKSTART.md) - Quick start guide
- [Workflow Diagrams](docs/workflows.md) - Visual process flows with Mermaid diagrams

## 🐛 Troubleshooting

### Common Issues

**Import errors**
```bash
pip install -r requirements.txt
```

**GPU not detected**
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

**Port already in use**
```bash
./scripts/launch.sh --port 8080
```

**Application won't stop**
```bash
./scripts/stop.sh --force
```

## 🎯 Examples

### Parse a Single PDF with Multiple Formats
1. Select **Markdown**, **HTML**, and **JSON** checkboxes
2. Upload your PDF through the web interface
3. Click "Parse Document"
4. Watch the progress updates
5. View the extracted content in all three formats

### Batch Process Multiple Documents with Progress Tracking
1. Copy 10 PDFs to the `input/` directory
2. Select desired output formats (e.g., Markdown and HTML)
3. Click "Process Batch" in the web interface
4. Watch the progress bar showing "Processing file 3/10..."
5. All 10 documents are parsed and saved to `output/` in selected formats

### Use GPU Acceleration
```bash
./scripts/launch.sh --gpu --detached
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

You can also use the enhanced parser programmatically:

```python
from docling_parser import DoclingParser

# Initialize parser
parser = DoclingParser(use_gpu=False, output_dir="output")

# Parse single document with all features
result = parser.parse_document(
    "document.pdf",
    output_formats=['markdown', 'html', 'json'],
    export_figures=True,
    export_multimodal=False,
    ocr_engine='easyocr',
    force_ocr=False
)
print(result)

# Parse batch with advanced features
results = parser.parse_batch(
    "input",
    output_formats=['markdown', 'json'],
    export_figures=True,
    ocr_engine='tesseract',
    force_ocr=True
)
for result in results:
    status = "✓" if result['status'] == 'success' else "✗"
    figures = result.get('figure_count', 0)
    print(f"{status} {result['input_file']}: {figures} figures")

# Get available OCR engines
ocr_engines = parser.get_ocr_engines()
print(f"Available OCR engines: {ocr_engines}")

# Parse CSV file
csv_result = parser.parse_document(
    "data.csv",
    output_formats=['markdown', 'html', 'json']
)

# Parse XBRL file
xbrl_result = parser.parse_document(
    "financial.xbrl",
    output_formats=['markdown', 'json']
)
```

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