# 🚀 Getting Started with Docling Factory

## Quick Start (3 Steps)

### Step 1: Prerequisites

Ensure you have:
- Python 3.8 or higher
- pip package manager
- **Podman or Docker** (for OpenSearch/RAG features)
- **Ollama** (for local LLM/RAG features)
- (Optional) CUDA-compatible GPU for acceleration

### Step 2: Installation

```bash
# Clone or navigate to the project directory
cd docling-factory

# Run setup script (creates venv and installs dependencies)
./scripts/setup.sh

# For GPU support (requires CUDA)
./scripts/setup.sh --gpu
```

### Step 3: Launch Application

```bash
# Standard launch (recommended)
./scripts/launch.sh

# Or with options
./scripts/launch.sh --detached --port 8080 --gpu
```

Open your browser to: **http://localhost:7860**

---

## RAG Setup (Optional)

For document chat features:

### 1. Install Ollama

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Pull required models
ollama pull llama3.2:latest
ollama pull granite-embedding:30m
```

### 2. Start OpenSearch

```bash
# Using Podman
podman-compose -f docker-compose-opensearch.yml up -d

# Or using Docker
docker-compose -f docker-compose-opensearch.yml up -d
```

### 3. Initialize RAG Engine

1. Launch `app_enhanced.py`
2. Go to "💬 Chat with Documents" tab
3. Select models and click "🔧 Initialize RAG Engine"
4. Parse documents with "Index for RAG" enabled
5. Start chatting!

---

## Basic Usage

### Individual File Processing

1. Open http://localhost:7860
2. **Configure Settings:**
   - Select output formats (Markdown, HTML, JSON, DocTags)
   - Enable features (Extract Figures, Multimodal Export)
   - Choose OCR engine (RapidOCR, EasyOCR, Tesseract, macOS Vision)
3. Go to **"📤 Individual Upload"** tab
4. Upload document(s)
5. Click **"🚀 Parse Document"**
6. View results in format tabs

### Batch Processing

1. Place documents in `input/` directory
2. Configure settings
3. Go to **"📦 Batch Processing"** tab
4. Click **"🚀 Process Batch"**
5. Check `output/` directory for results

---

## Important Notes

### ⚠️ Always Use Launch Script or Activate venv

**Correct:**
```bash
./scripts/launch.sh
```

**Or manually:**
```bash
source venv/bin/activate
python app_enhanced.py
```

**Wrong (will cause errors):**
```bash
python app_enhanced.py  # ❌ Missing venv activation
```

### Script Commands

```bash
# Start application
./scripts/launch.sh [--detached] [--port PORT] [--gpu] [--share]

# Stop application
./scripts/stop.sh [--force]

# Check status
./scripts/status.sh

# Run tests
./scripts/test.sh
```

---

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
./scripts/launch.sh --port 8080
```

**Dependencies not installed:**
```bash
./scripts/setup.sh
```

**Application won't stop:**
```bash
./scripts/stop.sh --force
```

**Check logs:**
```bash
tail -f logs/app.log
```

---

## Next Steps

- **Full Documentation**: [`docs/README.md`](README.md)
- **Architecture**: [`docs/ARCHITECTURE.md`](ARCHITECTURE.md)
- **Troubleshooting**: [`docs/TROUBLESHOOTING.md`](TROUBLESHOOTING.md)
- **Workflows**: [`docs/workflows.md`](workflows.md)

---

**Made with ❤️ for production-scale document processing**