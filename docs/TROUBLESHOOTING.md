# Troubleshooting Guide

Common issues and solutions for Docling Factory.

## Quick Diagnostics

```bash
# Check application status
./scripts/status.sh

# View logs
tail -f logs/app.log

# Check Python environment
which python
echo $VIRTUAL_ENV

# Check installed packages
pip list | grep -E "docling|gradio|easyocr"
```

---

## Common Issues

### 1. EasyOCR "Not Installed" Error

**Problem**: Error appears even though EasyOCR is installed.

**Root Cause**: Application running outside virtual environment.

**Solution**:
```bash
# Always use launch script
./scripts/launch.sh

# OR activate venv manually
source venv/bin/activate
python app_enhanced.py
```

**Prevention**: Never run `python app_enhanced.py` without activating venv first.

---

### 2. Port Already in Use

**Problem**: `Address already in use: 7860`

**Solutions**:
```bash
# Check what's using the port
lsof -i :7860

# Stop existing process
./scripts/stop.sh

# Use different port
./scripts/launch.sh --port 8080
```

---

### 3. OpenSearch Connection Issues

**Problem**: Cannot connect to OpenSearch or RAG features don't work.

**Solutions**:
```bash
# Start OpenSearch
podman-compose -f docker-compose-opensearch.yml up -d
# OR
docker-compose -f docker-compose-opensearch.yml up -d

# Verify it's running
curl -X GET "http://localhost:9200" -u admin:admin -k

# Check container status
podman ps | grep opensearch
# OR
docker ps | grep opensearch

# Restart if needed
podman-compose -f docker-compose-opensearch.yml restart
```

---

### 4. Ollama Model Not Found

**Problem**: Selected LLM model not available.

**Solutions**:
```bash
# List available models
ollama list

# Pull required model
ollama pull llama3.2:latest
ollama pull granite-embedding:30m

# Verify Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve
```

---

### 5. GPU Not Working

**Problem**: GPU acceleration not being used.

**Solutions**:
```bash
# Check if GPU is available
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"

# Install GPU requirements
source venv/bin/activate
pip install -r requirements-gpu.txt

# Launch with GPU flag
./scripts/launch.sh --gpu
```

---

### 6. Dependency Conflicts

**Problem**: Errors about numpy, setuptools, or package version conflicts.

**Solution**:
```bash
# Reinstall dependencies in correct order
source venv/bin/activate
pip install --upgrade pip
pip install "setuptools<80"
pip install "numpy>=1.24.0,<2.0.0"
pip install opencv-python-headless
pip install torch torchvision
pip install -r requirements.txt
```

---

### 7. Chat History Format Error

**Problem**: `Data incompatible with messages format`

**Solution**: Ensure you're using `app_enhanced.py`, not the old `app.py`.

```bash
./scripts/launch.sh  # Automatically uses app_enhanced.py
```

---

### 8. Application Won't Stop

**Problem**: Application continues running after stop command.

**Solutions**:
```bash
# Force stop
./scripts/stop.sh --force

# Manual kill
ps aux | grep "python.*app"
kill -9 <PID>
```

---

### 9. Memory Issues

**Problem**: Out of memory errors during processing.

**Solutions**:
1. Use smaller models:
   - LLM: `llama3.2:latest` (2GB) instead of larger models
   - Embedding: `granite-embedding:30m` (62MB)

2. Reduce chunk size in `rag_engine.py`:
   ```python
   self.text_splitter = RecursiveCharacterTextSplitter(
       chunk_size=500,  # Reduced from 1000
       chunk_overlap=100,  # Reduced from 200
   )
   ```

3. Limit context chunks:
   - Set `top_k=3` instead of `top_k=5`

4. Process fewer documents at once

---

### 10. Slow Response Times

**Problem**: RAG responses are slow.

**Solutions**:
1. Use faster models (llama3.2:latest)
2. Reduce context chunks (lower top_k value)
3. Enable GPU acceleration
4. Optimize OpenSearch:
   ```bash
   export OPENSEARCH_JAVA_OPTS="-Xms1g -Xmx1g"
   ```

---

### 11. Import Errors

**Problem**: `ModuleNotFoundError` or import errors.

**Solutions**:
```bash
# Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt

# For GPU version
pip install -r requirements-gpu.txt

# Verify installation
python -c "import docling; import gradio; print('OK')"
```

---

### 12. OCR Engine Issues

**Problem**: OCR engine not working or not found.

**Solutions**:

**RapidOCR** (Recommended):
```bash
# Built-in with Docling 2.74.0+
pip install --upgrade docling
```

**EasyOCR**:
```bash
source venv/bin/activate
pip install easyocr
```

**Tesseract**:
```bash
# macOS
brew install tesseract

# Ubuntu
sudo apt-get install tesseract-ocr

# Windows
# Download from https://github.com/UB-Mannheim/tesseract/wiki
```

---

### 13. RAG Engine Won't Initialize

**Problem**: RAG engine initialization fails.

**Checklist**:
```bash
# 1. Check OpenSearch
curl http://localhost:9200

# 2. Check Ollama
curl http://localhost:11434/api/tags

# 3. Check models
ollama list

# 4. Restart services
podman-compose -f docker-compose-opensearch.yml restart
ollama serve
```

---

### 14. No Results When Chatting

**Possible Causes**:
1. No documents indexed
2. Query doesn't match document content
3. Top K too low

**Solutions**:
- Verify documents are indexed (check RAG Statistics)
- Try broader questions
- Increase Top K to 10
- Re-index documents

---

### 15. File Upload Errors

**Problem**: Cannot upload files or upload fails.

**Solutions**:
```bash
# Check file permissions
ls -la input/

# Check disk space
df -h

# Verify file format is supported
# Supported: PDF, DOCX, PPTX, XLSX, HTML, MD, TXT, CSV, XBRL
```

---

## Environment-Specific Issues

### macOS

**Issue**: Port 5000 conflicts with AirDrop
```bash
./scripts/launch.sh --port 7860  # Use different port
```

**Issue**: macOS Vision OCR not working
```bash
# Ensure you're on macOS 10.15+
# Select "macOS Vision OCR" in UI
```

### Linux

**Issue**: Tesseract not found
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

### Windows

**Issue**: Scripts won't run
```bash
# Use Git Bash or WSL
# Or run Python directly:
python app_enhanced.py
```

---

## Logging and Debugging

### Enable Debug Logging

Edit `app_enhanced.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### View Logs

```bash
# Real-time logs
tail -f logs/app.log

# Last 100 lines
tail -100 logs/app.log

# Search for errors
grep -i error logs/app.log
```

### Check System Resources

```bash
# CPU and memory usage
top

# Disk space
df -h

# Process list
ps aux | grep python
```

---

## Getting Help

If you're still experiencing issues:

1. **Check logs**: `tail -f logs/app.log`
2. **Run diagnostics**: `./scripts/status.sh`
3. **Review documentation**: 
   - [Getting Started](GETTING_STARTED.md)
   - [Comprehensive Guide](COMPREHENSIVE_GUIDE.md)
   - [Architecture](ARCHITECTURE.md)
4. **Check GitHub issues**: Search for similar problems
5. **Create new issue**: Provide logs and system information

---

## System Requirements

### Minimum Requirements
- Python 3.8+
- 4GB RAM
- 10GB disk space
- Modern CPU

### Recommended Requirements
- Python 3.10+
- 8GB RAM
- 20GB disk space
- Multi-core CPU
- (Optional) CUDA-compatible GPU

### For RAG Features
- Additional 4GB RAM
- Podman/Docker installed
- Ollama installed
- 10GB disk space for models

---

**Made with ❤️ for production-scale document processing**