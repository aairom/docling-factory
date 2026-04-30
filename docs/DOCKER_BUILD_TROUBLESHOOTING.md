# Docker Build Troubleshooting Guide

## Issue: Docker Build Timeout

### Error Message
```
failed to solve: DeadlineExceeded: no active session for ugpmsy5netegji8mtrxs2ht6t: context deadline exceeded
```

### Root Cause
The Docker build is timing out because:
1. **Heavy dependencies**: PyTorch, EasyOCR, and ML libraries are very large (2-3 GB)
2. **Slow network**: Downloading packages can take 20+ minutes
3. **Docker BuildKit timeout**: Default timeout is too short for large builds

## Solutions

### Solution 1: Use Pre-built Images (Recommended)

Instead of building from scratch, pull the pre-built images:

```bash
# Pull the LiteLLM image (already built)
docker pull ghcr.io/berriai/litellm:main-latest

# Pull OpenSearch image (already built)
docker pull opensearchproject/opensearch:2.11.0

# For the application, use the optimized Dockerfile
docker-compose build --build-arg BUILDKIT_INLINE_CACHE=1 docling-factory-cpu
```

### Solution 2: Increase Docker Build Timeout

Increase the BuildKit timeout:

```bash
# Set environment variable for longer timeout (30 minutes)
export DOCKER_BUILDKIT=1
export BUILDKIT_STEP_LOG_MAX_SIZE=50000000
export BUILDKIT_STEP_LOG_MAX_SPEED=10000000

# Build with increased timeout
docker-compose build --no-cache --progress=plain
```

### Solution 3: Use Optimized Dockerfile

Use the optimized Dockerfile that builds dependencies in stages:

```bash
# Update docker-compose.yml to use Dockerfile.optimized
docker-compose build -f Dockerfile.optimized docling-factory-cpu
```

Or manually:

```bash
docker build -f Dockerfile.optimized -t docling-factory:latest .
```

### Solution 4: Build with More Resources

Allocate more resources to Docker:

1. **Docker Desktop Settings**:
   - Go to Docker Desktop → Settings → Resources
   - Increase CPUs to 4+ cores
   - Increase Memory to 8+ GB
   - Increase Swap to 2+ GB

2. **Build with more memory**:
   ```bash
   docker build --memory=8g --memory-swap=10g -f Dockerfile -t docling-factory:latest .
   ```

### Solution 5: Use Docker Compose Build with Parallel Builds Disabled

```bash
# Build services one at a time
docker-compose build opensearch
docker-compose build litellm-db
docker-compose build litellm
docker-compose build docling-factory-cpu
```

### Solution 6: Skip Heavy Dependencies (Quick Start)

Create a minimal requirements file for faster builds:

```bash
# Create requirements-minimal.txt
cat > requirements-minimal.txt << 'EOF'
# Core only - no ML/OCR
docling>=2.0.0
gradio>=4.0.0
opensearch-py>=2.4.0
langchain>=0.1.0
ollama>=0.1.0
litellm>=1.0.0
httpx>=0.24.0
opentelemetry-api>=1.20.0
opentelemetry-sdk>=1.20.0
traceloop-sdk>=0.30.0
EOF

# Build with minimal requirements
docker build --build-arg REQUIREMENTS_FILE=requirements-minimal.txt -t docling-factory:minimal .
```

### Solution 7: Use Multi-stage Build with Cache

```bash
# Enable BuildKit cache
export DOCKER_BUILDKIT=1

# Build with cache mount
docker build \
  --cache-from=docling-factory:latest \
  --build-arg BUILDKIT_INLINE_CACHE=1 \
  -t docling-factory:latest \
  -f Dockerfile .
```

## Recommended Workflow

### For Development (Fast)

1. **Use pre-built services**:
   ```bash
   # Start only pre-built services
   docker-compose up -d opensearch litellm-db litellm
   ```

2. **Run application locally**:
   ```bash
   # Install dependencies locally (one-time)
   pip install -r requirements.txt
   
   # Run the application
   python app_enhanced.py
   ```

3. **Configure to use Docker services**:
   - OpenSearch: `http://localhost:9200`
   - LiteLLM: `http://localhost:4000`
   - Ollama: `http://localhost:11434` (if running locally)

### For Production (Full Build)

1. **Build overnight or on powerful machine**:
   ```bash
   # Start build and let it run
   nohup docker-compose build > build.log 2>&1 &
   
   # Monitor progress
   tail -f build.log
   ```

2. **Or use CI/CD pipeline** with longer timeouts

3. **Or use pre-built images** from container registry

## Quick Start Without Building

If you just want to test LiteLLM integration without building:

```bash
# 1. Start only the services that don't need building
docker-compose up -d opensearch litellm-db litellm

# 2. Install Python dependencies locally
pip install -r requirements.txt

# 3. Set environment variables
export OPENSEARCH_HOST=localhost
export OPENSEARCH_PORT=9200
export LITELLM_API_BASE=http://localhost:4000
export LITELLM_API_KEY=sk-1234
export OLLAMA_BASE_URL=http://localhost:11434

# 4. Run the application locally
python app_enhanced.py

# 5. Access the UI
open http://localhost:7860
```

## Verifying Services

Check if services are running:

```bash
# Check all services
docker-compose ps

# Check LiteLLM
curl http://localhost:4000/health

# Check OpenSearch
curl http://localhost:9200

# Check application (if running in Docker)
curl http://localhost:7860
```

## Alternative: Use Docker Hub Images

If building is consistently failing, consider:

1. **Push to Docker Hub** from a machine that can build successfully
2. **Pull from Docker Hub** on machines with build issues

```bash
# On build machine
docker build -t yourusername/docling-factory:latest .
docker push yourusername/docling-factory:latest

# On deployment machine
docker pull yourusername/docling-factory:latest
docker-compose up -d
```

## Performance Tips

1. **Use SSD**: Docker builds are I/O intensive
2. **Fast internet**: Large downloads (PyTorch ~2GB)
3. **More RAM**: 8GB+ recommended for building
4. **More CPU cores**: 4+ cores recommended
5. **Clean Docker cache** periodically:
   ```bash
   docker system prune -a
   docker builder prune -a
   ```

## Still Having Issues?

If none of these solutions work:

1. **Check Docker logs**:
   ```bash
   docker-compose logs -f
   ```

2. **Check system resources**:
   ```bash
   docker stats
   ```

3. **Try building individual components**:
   ```bash
   # Test if Python can install packages
   docker run -it python:3.11-slim bash
   pip install litellm
   ```

4. **Use the minimal setup** (see Solution 6) for testing

5. **Report the issue** with full logs:
   ```bash
   docker-compose build --no-cache --progress=plain > build-debug.log 2>&1