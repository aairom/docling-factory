# 🏭 Docling Factory

A powerful, production-ready document parsing application built with [Docling](https://github.com/docling-project/docling) and [Docling-Parse](https://github.com/docling-project/docling-parse). Parse PDF, DOCX, PPTX, XLSX, HTML, and more with both individual and batch processing modes, featuring multiple output formats, real-time progress tracking, and deployment-ready Docker and Kubernetes configurations.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Docling](https://img.shields.io/badge/docling-2.0+-purple.svg)

## ✨ Features

- 🎯 **Dual Processing Modes**
  - Individual file upload and processing
  - Batch processing of entire directories
  
- ⚡ **GPU Acceleration**
  - Optional GPU support for faster processing
  - Automatic fallback to CPU mode
  
- 📊 **Multiple Output Formats**
  - **Markdown** (.md) - Human-readable content
  - **HTML** (.html) - Web-ready format
  - **JSON** (.json) - Structured data for integration
  - Select any combination of formats with checkboxes
  
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
  
- 🔧 **Enhanced Parsing**
  - Powered by **Docling** and **Docling-Parse**
  - Advanced document structure recognition
  - Improved table and layout detection

## 📋 Supported Formats

- PDF (`.pdf`)
- Microsoft Word (`.docx`, `.doc`)
- Microsoft PowerPoint (`.pptx`)
- Microsoft Excel (`.xlsx`)
- HTML (`.html`)
- Markdown (`.md`)
- Plain Text (`.txt`)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) CUDA-compatible GPU for GPU acceleration

### Installation

1. **Clone or download this repository**

```bash
cd docling-factory
```

2. **Run the setup script**

```bash
# For CPU version (recommended for most users)
./scripts/setup.sh

# For GPU version (requires CUDA)
./scripts/setup.sh --gpu
```

3. **Start the application**

```bash
./scripts/launch.sh
```

4. **Open your browser**

Navigate to `http://localhost:7860`

## 📖 Usage

### Individual File Processing

1. Open the web interface at `http://localhost:7860`
2. **Select output formats** using the checkboxes (Markdown, HTML, JSON)
3. Navigate to the **"📤 Individual Upload"** tab
4. (Optional) Enable GPU acceleration
5. Click **"Upload Document"** and select your file
6. Click **"🚀 Parse Document"**
7. Watch the **real-time progress** updates
8. View results in separate tabs for each format

### Batch Processing

1. Place documents in the `input/` directory
2. Open the web interface
3. **Select output formats** using the checkboxes (Markdown, HTML, JSON)
4. Navigate to the **"📦 Batch Processing"** tab
5. (Optional) Enable GPU acceleration
6. Click **"🚀 Process Batch"**
7. Watch the **progress bar** and status updates
8. View processing summary and results in the `output/` directory

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
├── QUICKSTART.md          # Quick start guide
├── docs/                  # Documentation
│   ├── README.md          # Detailed documentation
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

You can also use the parser programmatically:

```python
from docling_parser import DoclingParser

# Initialize parser
parser = DoclingParser(use_gpu=False, output_dir="output")

# Parse single document
result = parser.parse_document("document.pdf")
print(result)

# Parse batch
results = parser.parse_batch("input")
for result in results:
    print(f"{result['input_file']}: {result['status']}")
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project uses the Docling library. Please refer to the [Docling license](https://github.com/docling-project/docling) for terms and conditions.

## 🔗 Links

- [Docling Documentation](https://docling-project.github.io/docling/)
- [Docling GitHub](https://github.com/docling-project/docling)
- [Docling-Parse GitHub](https://github.com/docling-project/docling-parse)
- [Gradio Documentation](https://www.gradio.app/docs/)

## 📞 Support

For issues related to:
- **This application**: Open an issue in this repository
- **Docling library**: Visit [Docling GitHub](https://github.com/docling-project/docling)

## 🙏 Acknowledgments

- [Docling](https://github.com/docling-project/docling) - The powerful document parsing library
- [Docling-Parse](https://github.com/docling-project/docling-parse) - Enhanced parsing capabilities
- [Gradio](https://www.gradio.app/) - The amazing UI framework

---

**Docling Factory** - Made with ❤️ for production-scale document processing