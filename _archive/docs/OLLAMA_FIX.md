# Ollama Connection Fix

## Problem
The RAG Statistics page was showing Ollama as disconnected even though Ollama was running:
```
OpenSearch: ✅ Connected
Ollama: ❌ Disconnected
Embedding Model: ❌ Not Found
LLM Model: ❌ Not Found
```

## Root Cause
The `health_check()` method in `rag_engine.py` was incorrectly parsing the Ollama API response. 

### Technical Details
When calling `ollama.Client().list()`, the response is a `ListResponse` object containing `Model` objects, not a dictionary. Each `Model` object has a `.model` attribute (not `.name`).

**Old Code (Incorrect):**
```python
models = client.list()
model_names = [m['name'] for m in models.get('models', [])]
```

**New Code (Correct):**
```python
response = client.list()
model_names = []
if hasattr(response, 'models'):
    model_names = [m.model for m in response.models]
elif isinstance(response, dict) and 'models' in response:
    model_names = [m.get('name', m.get('model', '')) for m in response['models']]
```

## Solution Applied
Updated `rag_engine.py` line 488-500 to correctly extract model names from the Ollama `ListResponse` object.

## Verification
After the fix, health check shows all systems connected:
```
opensearch: ✅ True
ollama: ✅ True
embedding_model: ✅ True
llm_model: ✅ True
```

## How to Verify the Fix

1. **Restart the application:**
   ```bash
   ./scripts/launch.sh
   ```

2. **Check RAG Statistics:**
   - Open the app in your browser
   - Go to "📊 RAG Statistics" tab
   - Click "🔄 Refresh Statistics"
   - You should now see all ✅ Connected

3. **Initialize RAG Engine:**
   - Go to "💬 Chat with Documents" tab
   - Select models (granite-embedding:30m, llama3.2:latest)
   - Click "🔧 Initialize RAG Engine"
   - You should see: "✅ RAG Engine initialized with llama3.2:latest and granite-embedding:30m"

## Related Files
- `rag_engine.py` - Fixed health_check() method
- `app_enhanced.py` - Uses health_check() for statistics display

## Testing
Run this command to verify the fix:
```bash
python3 -c "
from rag_engine import RAGEngine
rag = RAGEngine(enable_tracing=False)
health = rag.health_check()
print('Health Check:', health)
"
```

Expected output:
```
Health Check: {
    'opensearch': True,
    'ollama': True,
    'embedding_model': True,
    'llm_model': True
}