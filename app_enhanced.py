"""
Docling Document Parser - Enhanced Gradio UI Application with RAG
A comprehensive interface for parsing documents and chatting with them using:
- Multiple output formats (Markdown, HTML, JSON, DocTags)
- Multimodal export with embedded images
- Figure extraction
- Full page OCR with multiple engine options
- RAG (Retrieval-Augmented Generation) with OpenSearch and Ollama
- OpenLLMetry observability dashboard
"""

import gradio as gr
import os
import json
from pathlib import Path
from datetime import datetime
from docling_parser import DoclingParser
from rag_engine import RAGEngine
import logging
import ollama
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize components
parser = None
rag_engine = None
chat_history = []

# Configuration
OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "localhost")
OPENSEARCH_PORT = int(os.getenv("OPENSEARCH_PORT", "9200"))
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


def check_ocr_availability():
    """Check which OCR engines are available."""
    available_engines = [("No OCR", "none")]
    
    # Check EasyOCR
    try:
        import easyocr
        available_engines.append(("EasyOCR (Deep Learning) ✓", "easyocr"))
    except ImportError:
        available_engines.append(("EasyOCR (Deep Learning) ✗ Not Installed", "easyocr_unavailable"))
    
    # Check Tesseract
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        available_engines.append(("Tesseract OCR (Traditional) ✓", "tesseract"))
    except Exception:
        available_engines.append(("Tesseract OCR (Traditional) ✗ Not Installed", "tesseract_unavailable"))
    
    # Check macOS Vision
    import platform
    if platform.system() == 'Darwin':
        available_engines.append(("macOS Vision OCR ✓", "ocrmac"))
    else:
        available_engines.append(("macOS Vision OCR ✗ macOS Only", "ocrmac_unavailable"))
    
    return available_engines


def initialize_parser(use_gpu: bool):
    """Initialize or reinitialize the parser with GPU settings."""
    global parser
    parser = DoclingParser(use_gpu=use_gpu, output_dir="output")
    return f"Parser initialized with {'GPU' if use_gpu else 'CPU'} mode"


def initialize_rag(embedding_model: str, llm_model: str, enable_tracing: bool = True):
    """Initialize RAG engine with selected models."""
    global rag_engine
    try:
        rag_engine = RAGEngine(
            opensearch_host=OPENSEARCH_HOST,
            opensearch_port=OPENSEARCH_PORT,
            ollama_base_url=OLLAMA_BASE_URL,
            embedding_model=embedding_model,
            llm_model=llm_model,
            enable_tracing=enable_tracing
        )
        return f"✅ RAG Engine initialized with {llm_model} and {embedding_model}"
    except Exception as e:
        logger.error(f"Error initializing RAG: {e}")
        return f"❌ Error: {str(e)}"


def get_available_ollama_models() -> List[str]:
    """Get list of available Ollama models."""
    try:
        client = ollama.Client(host=OLLAMA_BASE_URL)
        response = client.list()
        
        # The response is a ListResponse object with a 'models' attribute
        if hasattr(response, 'models'):
            models = response.models
        elif isinstance(response, dict) and 'models' in response:
            models = response['models']
        elif isinstance(response, list):
            models = response
        else:
            logger.warning(f"Unexpected Ollama response format: {type(response)}")
            return ["llama3.2:latest"]  # Fallback
        
        # Extract model names - each model has a 'model' attribute
        model_names = []
        for m in models:
            if hasattr(m, 'model'):
                model_names.append(m.model)
            elif isinstance(m, dict):
                model_names.append(m.get('name', m.get('model', 'unknown')))
        
        return model_names if model_names else ["llama3.2:latest"]
    except Exception as e:
        logger.error(f"Error fetching Ollama models: {e}")
        return ["llama3.2:latest"]  # Fallback to default


def parse_single_file(files, use_gpu, markdown_check, html_check, json_check, doctags_check,
                     export_figures, export_multimodal, ocr_engine, force_ocr, index_for_rag):
    """Parse uploaded file(s) with selected options and optionally index for RAG."""
    if files is None:
        return "⚠️ No file uploaded", "", "", "", ""
    
    # Convert single file to list for uniform processing
    if not isinstance(files, list):
        files = [files]
    
    if len(files) == 0:
        return "⚠️ No file uploaded", "", "", "", ""
    
    # Determine output formats
    output_formats = []
    if markdown_check:
        output_formats.append('markdown')
    if html_check:
        output_formats.append('html')
    if json_check:
        output_formats.append('json')
    if doctags_check:
        output_formats.append('doctags')
    
    if not output_formats:
        return "⚠️ Please select at least one output format", "", "", "", ""
    
    try:
        # Validate OCR engine selection
        if ocr_engine.endswith('_unavailable'):
            return (
                f"⚠️ **OCR Engine Not Available**\n\nThe selected OCR engine is not installed or unavailable. "
                f"Please select a different OCR engine or choose 'No OCR'.",
                "", "", "", ""
            )
        
        # Initialize parser if needed
        if parser is None or parser.use_gpu != use_gpu:
            initialize_parser(use_gpu)
        
        # Process multiple files
        all_results = []
        combined_markdown = []
        combined_html = []
        combined_json = []
        all_progress = []
        total_indexed = 0
        
        for idx, file in enumerate(files):
            progress_messages = []
            
            def progress_callback(msg):
                progress_messages.append(msg)
            
            file_progress = f"\n{'='*60}\n📄 Processing file {idx+1}/{len(files)}: {Path(file.name).name}\n{'='*60}\n"
            all_progress.append(file_progress)
            
            # Parse the document
            result = parser.parse_document(
                file.name,
                output_formats,
                export_figures=export_figures,
                export_multimodal=export_multimodal,
                ocr_engine=ocr_engine,
                force_ocr=force_ocr,
                progress_callback=progress_callback
            )
            
            all_progress.extend(progress_messages)
            
            if result["status"] == "success":
                all_results.append(result)
                
                # Read the generated outputs
                if 'markdown' in result['outputs']:
                    with open(result['outputs']['markdown'], 'r', encoding='utf-8') as f:
                        content = f.read()
                        combined_markdown.append(f"# {Path(result['input_file']).name}\n\n{content}")
                
                if 'html' in result['outputs']:
                    with open(result['outputs']['html'], 'r', encoding='utf-8') as f:
                        content = f.read()
                        combined_html.append(f"<!-- {Path(result['input_file']).name} -->\n{content}")
                
                if 'json' in result['outputs']:
                    with open(result['outputs']['json'], 'r', encoding='utf-8') as f:
                        content = json.load(f)
                        combined_json.append({Path(result['input_file']).name: content})
                
                # Index for RAG if requested
                if index_for_rag and rag_engine and 'markdown' in result['outputs']:
                    try:
                        with open(result['outputs']['markdown'], 'r', encoding='utf-8') as f:
                            markdown_content = f.read()
                        index_result = rag_engine.index_document(
                            file_path=file.name,
                            content=markdown_content,
                            metadata={"parsed_at": result['timestamp']}
                        )
                        total_indexed += index_result['chunks_indexed']
                        all_progress.append(f"📚 RAG Indexing: {index_result['chunks_indexed']} chunks indexed")
                    except Exception as e:
                        all_progress.append(f"⚠️ RAG Indexing failed: {str(e)}")
            else:
                all_progress.append(f"❌ Error: {result['error']}")
        
        progress_text = "\n".join(all_progress)
        
        if len(all_results) == 0:
            return "❌ **All files failed to parse**", "", "", "", progress_text
        
        # Build combined status message
        status_msg = f"""
✅ **Successfully parsed {len(all_results)} of {len(files)} document(s)!**

"""
        
        for idx, result in enumerate(all_results, 1):
            status_msg += f"""
### Document {idx}: {Path(result['input_file']).name}
- **Pages:** {result.get('page_count', 'N/A')}
- **Timestamp:** {result['timestamp']}
- **Output Formats:** {', '.join(result['formats'])}
"""
            if result.get('figure_count', 0) > 0:
                status_msg += f"- **Figures Extracted:** {result['figure_count']}\n"
            
            if result.get('ocr_engine'):
                status_msg += f"- **OCR Engine:** {result['ocr_engine']}\n"
        
        if index_for_rag and total_indexed > 0:
            status_msg += f"\n📚 **Total RAG Chunks Indexed:** {total_indexed}\n"
        
        # Combine outputs
        markdown_output = "\n\n---\n\n".join(combined_markdown)
        html_output = "\n\n".join(combined_html)
        json_output = json.dumps(combined_json, indent=2) if combined_json else ""
        
        return status_msg, markdown_output, html_output, json_output, progress_text
            
    except Exception as e:
        logger.error(f"Error in parse_single_file: {str(e)}")
        import traceback
        return f"❌ **Error:** {str(e)}\n\n{traceback.format_exc()}", "", "", "", ""


def chat_with_documents(query: str, llm_model: str, temperature: float, top_k: int):
    """Chat with indexed documents using RAG."""
    global chat_history
    
    if not rag_engine:
        return "⚠️ Please initialize RAG engine first", chat_history
    
    if not query.strip():
        return "⚠️ Please enter a question", chat_history
    
    try:
        # Get response from RAG
        response = rag_engine.chat(query, top_k=int(top_k), temperature=float(temperature))
        
        # Format response
        answer = response['answer']
        sources = response.get('sources', [])
        
        if sources:
            answer += "\n\n**Sources:**\n"
            for source in sources:
                answer += f"- {Path(source).name}\n"
        
        # Add to chat history in Gradio 6.x Chatbot format: list of message dicts
        chat_history.append({"role": "user", "content": query})
        chat_history.append({"role": "assistant", "content": answer})
        
        return "", chat_history
        
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        import traceback
        error_detail = traceback.format_exc()
        logger.error(f"Full error: {error_detail}")
        return f"❌ Error: {str(e)}", chat_history


def clear_chat():
    """Clear chat history."""
    global chat_history
    chat_history = []
    return []


def list_indexed_documents():
    """List all indexed documents."""
    if not rag_engine:
        return "⚠️ RAG engine not initialized"
    
    try:
        docs = rag_engine.list_indexed_documents()
        if not docs:
            return "No documents indexed yet"
        
        doc_list = "## 📚 Indexed Documents\n\n"
        for doc in docs:
            doc_list += f"- {Path(doc).name}\n"
        
        return doc_list
    except Exception as e:
        return f"❌ Error: {str(e)}"


def get_rag_stats():
    """Get RAG engine statistics."""
    if not rag_engine:
        return "⚠️ RAG engine not initialized"
    
    try:
        stats = rag_engine.get_stats()
        health = rag_engine.health_check()
        
        stats_md = f"""
## 📊 RAG Statistics

### Index Stats
- **Total Chunks:** {stats.get('total_chunks', 0)}
- **Unique Documents:** {stats.get('unique_documents', 0)}
- **Index Size:** {stats.get('index_size', 0) / 1024 / 1024:.2f} MB

### Health Status
- **OpenSearch:** {'✅ Connected' if health.get('opensearch') else '❌ Disconnected'}
- **Ollama:** {'✅ Connected' if health.get('ollama') else '❌ Disconnected'}
- **Embedding Model:** {'✅ Available' if health.get('embedding_model') else '❌ Not Found'}
- **LLM Model:** {'✅ Available' if health.get('llm_model') else '❌ Not Found'}
"""
        return stats_md
    except Exception as e:
        return f"❌ Error: {str(e)}"


def get_openllmetry_dashboard():
    """Get OpenLLMetry observability dashboard info."""
    dashboard_info = """
## 🔍 OpenLLMetry Observability Dashboard

OpenLLMetry provides comprehensive observability for your LLM applications.

### Features
- **Trace LLM Calls:** Monitor all interactions with Ollama models
- **Performance Metrics:** Track latency, token usage, and costs
- **Error Tracking:** Identify and debug issues quickly
- **Request/Response Logging:** Full visibility into prompts and completions

### Access Dashboard
OpenLLMetry traces are automatically collected when RAG is enabled.

To view traces:
1. Traces are logged to the console
2. Export to observability platforms (Jaeger, Zipkin, etc.)
3. Use OpenTelemetry collectors for advanced analysis

### Current Status
"""
    
    if rag_engine:
        dashboard_info += "✅ **Tracing Active** - All RAG operations are being traced\n"
    else:
        dashboard_info += "⚠️ **Tracing Inactive** - Initialize RAG to enable tracing\n"
    
    dashboard_info += """
### Traced Operations
- Document indexing
- Embedding generation
- Semantic search
- LLM generation
- Chat interactions

### Configuration
Set environment variables to configure OpenLLMetry:
```bash
export TRACELOOP_API_KEY=your_key  # Optional: for Traceloop cloud
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318  # For local collector
```
"""
    
    return dashboard_info


# Create the enhanced Gradio interface
with gr.Blocks(title="Docling Parser with RAG") as app:
    gr.Markdown("""
    # 📄 Docling Document Parser with RAG
    
    Parse documents and chat with them using **Retrieval-Augmented Generation (RAG)** powered by:
    - **OpenSearch** for vector storage
    - **Ollama** for local LLM and embeddings
    - **OpenLLMetry** for observability
    """)
    
    # Global settings
    with gr.Accordion("⚙️ Global Settings", open=True):
        with gr.Row():
            gpu_toggle = gr.Checkbox(
                label="Enable GPU Acceleration",
                value=False,
                info="Enable if you have CUDA-compatible GPU"
            )
        
        # Output format selection
        gr.Markdown("### 📤 Output Formats")
        with gr.Row():
            markdown_check = gr.Checkbox(label="Markdown (.md)", value=True)
            html_check = gr.Checkbox(label="HTML (.html)", value=True)
            json_check = gr.Checkbox(label="JSON (.json)", value=True)
            doctags_check = gr.Checkbox(label="DocTags (.txt)", value=False)
        
        # Advanced features
        gr.Markdown("### 🚀 Advanced Features")
        with gr.Row():
            export_figures = gr.Checkbox(label="Extract Figures", value=False)
            export_multimodal = gr.Checkbox(label="Multimodal Export", value=False)
            index_for_rag = gr.Checkbox(label="Index for RAG", value=True, 
                                       info="Automatically index parsed documents for chat")
        
        # OCR settings
        gr.Markdown("### 🔍 OCR Settings")
        available_ocr_engines = check_ocr_availability()
        with gr.Row():
            ocr_engine = gr.Dropdown(
                choices=available_ocr_engines,
                value="none",
                label="OCR Engine",
                info="✓ = Available, ✗ = Not installed/unavailable"
            )
            force_ocr = gr.Checkbox(label="Force Full Page OCR", value=False,
                                   info="Force OCR even if text is extractable")
    
    with gr.Tabs() as tabs:
        # Tab 1: Document Upload & Parse
        with gr.Tab("📤 Upload & Parse"):
            gr.Markdown("Upload and parse documents with optional RAG indexing.")
            
            with gr.Row():
                with gr.Column(scale=1):
                    file_input = gr.File(
                        label="Upload Document(s)",
                        file_types=[".pdf", ".docx", ".doc", ".pptx", ".xlsx", ".html", ".md", ".txt", ".csv"],
                        file_count="multiple"
                    )
                    parse_btn = gr.Button("🚀 Parse Document(s)", variant="primary", size="lg")
                
                with gr.Column(scale=2):
                    status_output = gr.Markdown(label="Status")
                    progress_output = gr.Textbox(label="Processing Progress", lines=5)
            
            with gr.Tabs():
                with gr.Tab("📝 Markdown"):
                    markdown_output = gr.Textbox(label="Parsed Content", lines=15)
                with gr.Tab("🌐 HTML"):
                    html_output = gr.Textbox(label="HTML Content", lines=15)
                with gr.Tab("🔧 JSON"):
                    json_output = gr.Textbox(label="JSON Data", lines=15)
            
            parse_btn.click(
                fn=parse_single_file,
                inputs=[file_input, gpu_toggle, markdown_check, html_check, json_check, doctags_check,
                       export_figures, export_multimodal, ocr_engine, force_ocr, index_for_rag],
                outputs=[status_output, markdown_output, html_output, json_output, progress_output]
            )
        
        # Tab 2: Chat with Documents
        with gr.Tab("💬 Chat with Documents"):
            gr.Markdown("""
            Ask questions about your indexed documents using RAG.
            
            **Setup:**
            1. Initialize RAG engine below
            2. Parse documents with "Index for RAG" enabled
            3. Start chatting!
            """)
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### RAG Configuration")
                    
                    # Get available models
                    available_models = get_available_ollama_models()
                    
                    llm_dropdown = gr.Dropdown(
                        choices=available_models if available_models else ["llama3.2:latest"],
                        value=available_models[0] if available_models else "llama3.2:latest",
                        label="LLM Model",
                        info="Select Ollama model for chat"
                    )
                    
                    embedding_dropdown = gr.Dropdown(
                        choices=["granite-embedding:30m", "embeddinggemma:latest"] + available_models,
                        value="granite-embedding:30m",
                        label="Embedding Model",
                        info="Select embedding model"
                    )
                    
                    enable_tracing = gr.Checkbox(
                        label="Enable OpenLLMetry Tracing",
                        value=True,
                        info="Track all LLM operations"
                    )
                    
                    init_rag_btn = gr.Button("🔧 Initialize RAG Engine", variant="primary")
                    rag_status = gr.Markdown()
                    
                    gr.Markdown("### Chat Settings")
                    temperature = gr.Slider(0, 1, value=0.7, label="Temperature")
                    top_k = gr.Slider(1, 10, value=5, step=1, label="Context Chunks")
                    
                    gr.Markdown("### Indexed Documents")
                    refresh_docs_btn = gr.Button("🔄 Refresh List", size="sm")
                    indexed_docs = gr.Markdown()
                
                with gr.Column(scale=2):
                    chatbot = gr.Chatbot(
                        label="Chat",
                        height=500
                    )
                    query_input = gr.Textbox(
                        label="Ask a question",
                        placeholder="What is this document about?",
                        lines=2
                    )
                    with gr.Row():
                        send_btn = gr.Button("📤 Send", variant="primary")
                        clear_btn = gr.Button("🗑️ Clear Chat", variant="secondary")
            
            # RAG initialization
            init_rag_btn.click(
                fn=initialize_rag,
                inputs=[embedding_dropdown, llm_dropdown, enable_tracing],
                outputs=rag_status
            )
            
            # Chat functionality
            send_btn.click(
                fn=chat_with_documents,
                inputs=[query_input, llm_dropdown, temperature, top_k],
                outputs=[query_input, chatbot]
            )
            
            query_input.submit(
                fn=chat_with_documents,
                inputs=[query_input, llm_dropdown, temperature, top_k],
                outputs=[query_input, chatbot]
            )
            
            clear_btn.click(fn=clear_chat, outputs=chatbot)
            
            refresh_docs_btn.click(fn=list_indexed_documents, outputs=indexed_docs)
            
            # Auto-load indexed documents
            app.load(fn=list_indexed_documents, outputs=indexed_docs)
        
        # Tab 3: RAG Statistics
        with gr.Tab("📊 RAG Statistics"):
            gr.Markdown("Monitor your RAG system performance and health.")
            
            refresh_stats_btn = gr.Button("🔄 Refresh Statistics", variant="primary")
            stats_output = gr.Markdown()
            
            refresh_stats_btn.click(fn=get_rag_stats, outputs=stats_output)
            app.load(fn=get_rag_stats, outputs=stats_output)
        
        # Tab 4: OpenLLMetry Dashboard
        with gr.Tab("🔍 OpenLLMetry"):
            gr.Markdown("LLM Observability and Tracing Dashboard")
            
            refresh_dashboard_btn = gr.Button("🔄 Refresh Dashboard", variant="primary")
            dashboard_output = gr.Markdown()
            
            refresh_dashboard_btn.click(fn=get_openllmetry_dashboard, outputs=dashboard_output)
            app.load(fn=get_openllmetry_dashboard, outputs=dashboard_output)
    
    gr.Markdown("""
    ---
    ### 🚀 Quick Start
    1. **Start OpenSearch:** `podman-compose -f docker-compose-opensearch.yml up -d`
    2. **Verify Ollama:** `ollama list` to see available models
    3. **Initialize RAG:** Go to "Chat with Documents" tab and click "Initialize RAG Engine"
    4. **Parse & Index:** Upload documents with "Index for RAG" enabled
    5. **Chat:** Ask questions about your documents!
    
    ### 🔗 Powered By
    - [Docling](https://github.com/docling-project/docling) - Document parsing
    - [OpenSearch](https://opensearch.org/) - Vector database
    - [Ollama](https://ollama.ai/) - Local LLM runtime
    - [OpenLLMetry](https://github.com/traceloop/openllmetry) - LLM observability
    - [Gradio](https://www.gradio.app/) - Web interface
    """)


def launch_app(share=False, server_port=7860):
    """Launch the Gradio application."""
    # Ensure directories exist
    Path("input").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)
    Path("output/figures").mkdir(exist_ok=True)
    
    logger.info(f"Launching Docling Parser with RAG on port {server_port}")
    
    app.launch(
        share=share,
        server_port=server_port,
        server_name="0.0.0.0",
        show_error=True
    )


if __name__ == "__main__":
    launch_app()

# Made with Bob