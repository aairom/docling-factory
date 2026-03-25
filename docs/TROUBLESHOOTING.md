# Troubleshooting Guide

## EasyOCR "Not Installed" Error

### Problem
You see this error even though EasyOCR is installed:
```
❌ Error: EasyOCR is not installed. Please install it via `pip install easyocr`
```

### Root Cause
The application is running **outside** the virtual environment where EasyOCR is installed.

### Solution

**Option 1: Use the Launch Script (Recommended)**
```bash
./scripts/launch.sh
```

The launch script automatically:
- Activates the virtual environment
- Checks dependencies
- Runs the correct app file (`app_enhanced.py` or `app.py`)

**Option 2: Manual Launch**
```bash
# Activate virtual environment first
source venv/bin/activate

# Then run the app
python app_enhanced.py
```

**Option 3: Verify Installation**
```bash
# Check if EasyOCR is in the venv
source venv/bin/activate
python -c "import easyocr; print('EasyOCR version:', easyocr.__version__)"
```

### Prevention
Always use one of these methods to start the app:
1. `./scripts/launch.sh` (best)
2. `source venv/bin/activate && python app_enhanced.py`
3. Never run `python app_enhanced.py` without activating venv first

---

## Dependency Conflicts

### Problem
Errors about numpy, setuptools, or other package version conflicts.

### Solution
```bash
# Reinstall dependencies in the correct order
source venv/bin/activate
pip install --upgrade pip
pip install "setuptools<80"
pip install "numpy>=1.24.0,<2.0.0"
pip install opencv-python-headless
pip install torch torchvision
pip install -r requirements.txt
```

---

## Chat History Format Error

### Problem
```
Data incompatible with messages format
```

### Solution
This was fixed in `app_enhanced.py`. The chat history format now uses:
```python
[
    {"role": "user", "content": "query"},
    {"role": "assistant", "content": "response"}
]
```

Make sure you're using `app_enhanced.py`, not the old `app.py`.

---

## OpenSearch Connection Issues

### Problem
Cannot connect to OpenSearch or RAG features don't work.

### Solution
1. Start OpenSearch:
```bash
docker-compose up -d opensearch
```

2. Verify it's running:
```bash
curl -X GET "http://localhost:9200" -u admin:admin -k
```

3. Check environment variables:
```bash
export OPENSEARCH_HOST=localhost
export OPENSEARCH_PORT=9200
```

---

## Ollama Model Not Found

### Problem
Selected LLM model not available.

### Solution
1. Check available models:
```bash
ollama list
```

2. Pull required model:
```bash
ollama pull llama3.2:latest
```

3. Verify Ollama is running:
```bash
curl http://localhost:11434/api/tags
```

---

## GPU Not Working

### Problem
GPU acceleration not being used.

### Solution
1. Check if GPU is available:
```bash
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

2. Use GPU requirements:
```bash
source venv/bin/activate
pip install -r requirements-gpu.txt
```

3. Launch with GPU flag:
```bash
./scripts/launch.sh --gpu
```

---

## Port Already in Use

### Problem
```
Address already in use: 7860
```

### Solution
1. Check what's using the port:
```bash
lsof -i :7860
```

2. Stop the existing process:
```bash
./scripts/stop.sh
```

3. Or use a different port:
```bash
./scripts/launch.sh --port 8080
```

---

## Quick Diagnostic Commands

```bash
# Check Python environment
which python
python --version

# Check if in venv
echo $VIRTUAL_ENV

# Check installed packages
pip list | grep -E "easyocr|docling|gradio"

# Check app status
./scripts/status.sh

# View logs
tail -f logs/app.log
```

---

## Getting Help

If you're still experiencing issues:

1. Check the logs: `tail -f logs/app.log`
2. Run diagnostics: `./scripts/status.sh`
3. Review documentation: `docs/QUICKSTART.md`
4. Check GitHub issues: [Project Issues](https://github.com/your-repo/issues)