# RAG System Usage Guide

## Quick Start

### 1. Start Required Services

```bash
# Start OpenSearch
docker-compose up -d opensearch

# Start Ollama (if not already running)
ollama serve
```

### 2. Launch the Application

```bash
./scripts/launch.sh
```

### 3. Initialize RAG Engine

In the Gradio UI:

1. Go to the **"Chat with Documents"** tab
2. Scroll down to **"RAG Configuration"** section
3. Select your models:
   - **Embedding Model**: `granite-embedding:30m` (recommended)
   - **LLM Model**: `llama3.2:latest` (or any model you have)
4. Click **"Initialize RAG Engine"**
5. Wait for confirmation: ✅ RAG Engine initialized

### 4. Index Documents

**Option A: Upload and Index**
1. Go to **"Document Parser"** tab
2. Upload your PDF(s)
3. Check **"Index for RAG"** checkbox
4. Click **"Parse Document"**
5. Documents will be parsed and indexed automatically

**Option B: Batch Process**
1. Place PDFs in the `input/` folder
2. Go to **"Batch Processing"** tab
3. Check **"Index for RAG"** checkbox
4. Click **"Process All Files"**

### 5. Chat with Documents

1. Go to **"Chat with Documents"** tab
2. Type your question in the chat box
3. Adjust settings if needed:
   - **Temperature**: 0.0 (factual) to 1.0 (creative)
   - **Top K**: Number of document chunks to retrieve (default: 5)
4. Click **"Submit"** or press Enter
5. Get AI-powered answers based on your documents!

---

## Understanding the Status

### RAG Statistics Tab

Shows real-time status of your RAG system:

```
📊 RAG Statistics

### Index Stats
- Total Chunks: 156
- Unique Documents: 3
- Index Size: 2.45 MB

### Health Status
- OpenSearch: ✅ Connected
- Ollama: ✅ Connected
- Embedding Model: ✅ Available
- LLM Model: ✅ Available
```

**What Each Status Means:**

- **OpenSearch Connected**: Vector database is running and accessible
- **Ollama Connected**: LLM server is running
- **Embedding Model Available**: Selected embedding model is installed
- **LLM Model Available**: Selected chat model is installed

### Common Status Issues

#### ❌ OpenSearch: Disconnected
**Solution:**
```bash
docker-compose up -d opensearch
# Wait 30 seconds for startup
curl http://localhost:9200
```

#### ❌ Ollama: Disconnected  
**Solution:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start it
ollama serve
```

#### ❌ Embedding Model: Not Found
**Solution:**
```bash
ollama pull granite-embedding:30m
```

#### ❌ LLM Model: Not Found
**Solution:**
```bash
ollama pull llama3.2:latest
```

---

## OpenLLMetry Dashboard

The **OpenLLMetry** tab provides observability for your LLM interactions:

### Features
- **Trace LLM Calls**: See every interaction with Ollama
- **Performance Metrics**: Track latency and token usage
- **Error Tracking**: Identify and debug issues
- **Request/Response Logging**: Full conversation history

### Accessing the Dashboard

1. Go to **"OpenLLMetry"** tab in the UI
2. Follow the instructions to access the dashboard
3. View traces at: `http://localhost:3000` (if configured)

---

## Tips for Best Results

### 1. Document Preparation
- Use clear, well-formatted PDFs
- Enable OCR for scanned documents
- Break large documents into sections

### 2. Indexing Strategy
- Index related documents together
- Use descriptive filenames
- Re-index if documents are updated

### 3. Query Optimization
- Ask specific questions
- Reference document names if needed
- Use follow-up questions for clarification

### 4. Model Selection
- **Embedding Models**:
  - `granite-embedding:30m` - Fast, good quality
  - `mxbai-embed-large` - Higher quality, slower
  - `nomic-embed-text` - Balanced option

- **LLM Models**:
  - `llama3.2:latest` - Fast, good for most tasks
  - `llama3:latest` - More capable, slower
  - `granite3.3:latest` - IBM model, good for business docs

### 5. Performance Tuning
- **Temperature**: 
  - 0.0-0.3: Factual, deterministic
  - 0.4-0.7: Balanced
  - 0.8-1.0: Creative, varied

- **Top K**:
  - 3-5: Focused answers
  - 5-10: More context
  - 10+: Comprehensive but slower

---

## Troubleshooting

### RAG Engine Won't Initialize

**Check:**
1. OpenSearch is running: `docker ps | grep opensearch`
2. Ollama is running: `curl http://localhost:11434/api/tags`
3. Models are installed: `ollama list`

**Fix:**
```bash
# Restart services
docker-compose restart opensearch
ollama serve

# Reinstall models if needed
ollama pull granite-embedding:30m
ollama pull llama3.2:latest
```

### No Results When Chatting

**Possible Causes:**
1. No documents indexed
2. Query doesn't match document content
3. Top K too low

**Solutions:**
- Verify documents are indexed (check RAG Statistics)
- Try broader questions
- Increase Top K to 10

### Slow Responses

**Optimizations:**
1. Use smaller models (llama3.2 instead of llama3)
2. Reduce Top K
3. Enable GPU if available: `./scripts/launch.sh --gpu`

---

## Advanced Usage

### Custom Embedding Models

```python
# In the UI, select from dropdown or
# Pull new model first:
ollama pull nomic-embed-text
```

### Batch Indexing

```bash
# Place all PDFs in input/
ls input/*.pdf

# Use Batch Processing tab with "Index for RAG" checked
```

### Clearing the Index

```bash
# Stop the app
./scripts/stop.sh

# Remove OpenSearch data
docker-compose down -v

# Restart
docker-compose up -d opensearch
./scripts/launch.sh
```

---

## Example Workflow

### Scenario: Analyzing Business Reports

1. **Prepare**:
   ```bash
   # Start services
   docker-compose up -d opensearch
   ollama serve
   ./scripts/launch.sh
   ```

2. **Initialize**:
   - Go to "Chat with Documents" tab
   - Select models
   - Click "Initialize RAG Engine"

3. **Index Reports**:
   - Upload Q1, Q2, Q3 reports
   - Check "Index for RAG"
   - Parse each document

4. **Analyze**:
   - Ask: "What were the key revenue drivers in Q2?"
   - Ask: "Compare Q1 and Q3 performance"
   - Ask: "Summarize the main challenges across all quarters"

5. **Review**:
   - Check RAG Statistics for index size
   - View OpenLLMetry for performance metrics

---

## Need Help?

- **Documentation**: Check `docs/` folder
- **Troubleshooting**: See `TROUBLESHOOTING.md`
- **Quick Start**: See `START_HERE.md`
- **Architecture**: See `docs/ARCHITECTURE.md`

---

**Made with ❤️ by Bob**