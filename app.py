"""
Docling Document Parser - Gradio UI Application
A user-friendly interface for parsing documents using Docling library.
Enhanced with multiple output formats, progress tracking, and docling-parse integration.
"""

import gradio as gr
import os
import json
from pathlib import Path
from datetime import datetime
from docling_parser import DoclingParser
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize parser (will be set based on user selection)
parser = None


def initialize_parser(use_gpu: bool):
    """Initialize or reinitialize the parser with GPU settings."""
    global parser
    parser = DoclingParser(use_gpu=use_gpu, output_dir="output")
    return f"Parser initialized with {'GPU' if use_gpu else 'CPU'} mode"


def parse_single_file(file, use_gpu, markdown_check, html_check, json_check):
    """
    Parse a single uploaded file with selected output formats.
    
    Args:
        file: Uploaded file object from Gradio
        use_gpu: Boolean indicating whether to use GPU
        markdown_check: Boolean for Markdown output
        html_check: Boolean for HTML output
        json_check: Boolean for JSON output
        
    Returns:
        Tuple of (status_message, markdown_content, html_content, json_output, progress_text)
    """
    if file is None:
        return "No file uploaded", "", "", "", ""
    
    # Determine output formats based on checkboxes
    output_formats = []
    if markdown_check:
        output_formats.append('markdown')
    if html_check:
        output_formats.append('html')
    if json_check:
        output_formats.append('json')
    
    if not output_formats:
        return "⚠️ Please select at least one output format", "", "", "", ""
    
    try:
        # Initialize parser if needed
        if parser is None or parser.use_gpu != use_gpu:
            initialize_parser(use_gpu)
        
        progress_messages = []
        
        def progress_callback(msg):
            progress_messages.append(msg)
        
        # Parse the document
        result = parser.parse_document(file.name, output_formats, progress_callback)
        
        progress_text = "\n".join(progress_messages)
        
        if result["status"] == "success":
            markdown_content = ""
            html_content = ""
            json_content = ""
            
            # Read the generated outputs
            if 'markdown' in result['outputs']:
                with open(result['outputs']['markdown'], 'r', encoding='utf-8') as f:
                    markdown_content = f.read()
            
            if 'html' in result['outputs']:
                with open(result['outputs']['html'], 'r', encoding='utf-8') as f:
                    html_content = f.read()
            
            if 'json' in result['outputs']:
                with open(result['outputs']['json'], 'r', encoding='utf-8') as f:
                    json_content = json.dumps(json.load(f), indent=2)
            
            # Build status message
            status_msg = f"""
✅ **Successfully parsed document!**

- **Input File:** {Path(result['input_file']).name}
- **Pages:** {result.get('page_count', 'N/A')}
- **Timestamp:** {result['timestamp']}
- **Output Formats:** {', '.join(result['formats'])}

**Generated Files:**
"""
            for fmt, path in result['outputs'].items():
                status_msg += f"\n- **{fmt.upper()}:** `{path}`"
            
            return status_msg, markdown_content, html_content, json_content, progress_text
        else:
            error_msg = f"❌ **Error parsing document:**\n\n{result['error']}"
            return error_msg, "", "", "", progress_text
            
    except Exception as e:
        logger.error(f"Error in parse_single_file: {str(e)}")
        return f"❌ **Error:** {str(e)}", "", "", "", ""


def parse_batch_files(use_gpu, markdown_check, html_check, json_check, progress=gr.Progress()):
    """
    Parse all files in the input directory with progress tracking.
    
    Args:
        use_gpu: Boolean indicating whether to use GPU
        markdown_check: Boolean for Markdown output
        html_check: Boolean for HTML output
        json_check: Boolean for JSON output
        progress: Gradio progress tracker
        
    Returns:
        Status message with summary
    """
    # Determine output formats
    output_formats = []
    if markdown_check:
        output_formats.append('markdown')
    if html_check:
        output_formats.append('html')
    if json_check:
        output_formats.append('json')
    
    if not output_formats:
        return "⚠️ **Warning:** Please select at least one output format"
    
    try:
        # Initialize parser if needed
        if parser is None or parser.use_gpu != use_gpu:
            initialize_parser(use_gpu)
        
        input_dir = Path("input")
        if not input_dir.exists():
            return "❌ **Error:** Input directory not found. Please create an 'input' folder and add documents."
        
        # Get list of files
        files = []
        for ext in parser.get_supported_formats():
            files.extend(list(input_dir.glob(f"*{ext}")))
            files.extend(list(input_dir.glob(f"*{ext.upper()}")))
        
        if not files:
            return "⚠️ **Warning:** No files found in the input directory."
        
        # Progress callback
        def progress_callback(msg, current, total):
            if total > 0:
                progress((current / total), desc=msg)
        
        # Process files
        results = parser.parse_batch(input_dir, output_formats, progress_callback=progress_callback)
        
        # Generate summary
        successful = [r for r in results if r["status"] == "success"]
        failed = [r for r in results if r["status"] == "error"]
        
        summary = f"""
## 📊 Batch Processing Complete

### Summary
- **Total Files:** {len(results)}
- **Successful:** {len(successful)} ✅
- **Failed:** {len(failed)} ❌
- **Output Formats:** {', '.join(output_formats)}

### Processed Files
"""
        
        for result in results:
            status_icon = "✅" if result["status"] == "success" else "❌"
            file_name = Path(result['input_file']).name
            summary += f"\n{status_icon} **{file_name}**"
            
            if result["status"] == "success":
                summary += f" - {result.get('page_count', 'N/A')} pages"
                formats_list = ', '.join(result.get('formats', []))
                summary += f" ({formats_list})"
            else:
                summary += f" - Error: {result.get('error', 'Unknown error')}"
        
        summary += f"\n\n### Output Location\nAll parsed documents are saved in the `output/` directory with timestamps."
        
        progress(1.0, desc="Batch processing complete!")
        
        return summary
        
    except Exception as e:
        logger.error(f"Error in parse_batch_files: {str(e)}")
        return f"❌ **Error:** {str(e)}"


def list_output_files():
    """List all files in the output directory."""
    output_dir = Path("output")
    if not output_dir.exists():
        return "No output directory found."
    
    files = sorted(output_dir.glob("*.*"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    if not files:
        return "No output files found."
    
    file_list = "## 📁 Output Files\n\n"
    for file in files[:30]:  # Show last 30 files
        size = file.stat().st_size / 1024  # KB
        mtime = datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        file_type = file.suffix.upper()[1:]  # Remove dot and uppercase
        file_list += f"- **[{file_type}]** {file.name} ({size:.1f} KB) - {mtime}\n"
    
    if len(files) > 30:
        file_list += f"\n*... and {len(files) - 30} more files*"
    
    return file_list


def clear_outputs(older_than_days):
    """Clear old output files."""
    try:
        if parser is None:
            initialize_parser(False)
        
        parser.clear_output_directory(older_than_days if older_than_days > 0 else None)
        return f"✅ Output directory cleared (files older than {older_than_days} days)" if older_than_days > 0 else "✅ All output files cleared"
    except Exception as e:
        return f"❌ Error: {str(e)}"


# Create the Gradio interface
with gr.Blocks(title="Docling Document Parser") as app:
    gr.Markdown("""
    # 📄 Docling Document Parser
    
    Parse documents using the powerful Docling library with **docling-parse** integration. 
    Supports PDF, DOCX, PPTX, XLSX, HTML, and more with multiple output formats.
    
    Choose between **Individual Upload** mode or **Batch Processing** mode.
    """)
    
    # GPU toggle (global setting)
    with gr.Row():
        gpu_toggle = gr.Checkbox(
            label="Enable GPU Acceleration",
            value=False,
            info="Enable this if you have CUDA-compatible GPU and installed GPU requirements"
        )
    
    # Output format selection (global)
    gr.Markdown("### 📤 Output Formats")
    with gr.Row():
        markdown_check = gr.Checkbox(label="Markdown (.md)", value=True)
        html_check = gr.Checkbox(label="HTML (.html)", value=True)
        json_check = gr.Checkbox(label="JSON (.json)", value=True)
    
    with gr.Tabs() as tabs:
        # Tab 1: Individual Upload
        with gr.Tab("📤 Individual Upload"):
            gr.Markdown("Upload a single document to parse it immediately.")
            
            with gr.Row():
                with gr.Column(scale=1):
                    file_input = gr.File(
                        label="Upload Document",
                        file_types=[".pdf", ".docx", ".doc", ".pptx", ".xlsx", ".html", ".md", ".txt"]
                    )
                    parse_btn = gr.Button("🚀 Parse Document", variant="primary", size="lg")
                
                with gr.Column(scale=2):
                    status_output = gr.Markdown(label="Status")
                    progress_output = gr.Textbox(label="Processing Progress", lines=5, max_lines=10)
            
            with gr.Tabs():
                with gr.Tab("📝 Markdown"):
                    markdown_output = gr.Textbox(
                        label="Parsed Content (Markdown)",
                        lines=15,
                        max_lines=20
                    )
                
                with gr.Tab("🌐 HTML"):
                    html_output = gr.Textbox(
                        label="Parsed Content (HTML)",
                        lines=15,
                        max_lines=20
                    )
                
                with gr.Tab("🔧 JSON"):
                    json_output = gr.Textbox(
                        label="Structured Data (JSON)",
                        lines=15,
                        max_lines=20
                    )
            
            parse_btn.click(
                fn=parse_single_file,
                inputs=[file_input, gpu_toggle, markdown_check, html_check, json_check],
                outputs=[status_output, markdown_output, html_output, json_output, progress_output]
            )
        
        # Tab 2: Batch Processing
        with gr.Tab("📦 Batch Processing"):
            gr.Markdown("""
            Process all documents in the `input/` directory at once.
            
            **Instructions:**
            1. Place your documents in the `input/` folder
            2. Select desired output formats above
            3. Click the "Process Batch" button
            4. Check the `output/` folder for results
            """)
            
            batch_btn = gr.Button("🚀 Process Batch", variant="primary", size="lg")
            batch_output = gr.Markdown(label="Batch Processing Results")
            
            batch_btn.click(
                fn=parse_batch_files,
                inputs=[gpu_toggle, markdown_check, html_check, json_check],
                outputs=batch_output
            )
        
        # Tab 3: Output Management
        with gr.Tab("📁 Output Management"):
            gr.Markdown("View and manage output files.")
            
            with gr.Row():
                refresh_btn = gr.Button("🔄 Refresh File List", size="sm")
                clear_days = gr.Number(
                    label="Clear files older than (days)",
                    value=0,
                    minimum=0,
                    info="Set to 0 to clear all files"
                )
                clear_btn = gr.Button("🗑️ Clear Outputs", variant="stop", size="sm")
            
            file_list_output = gr.Markdown(label="Output Files")
            clear_status = gr.Markdown(label="Clear Status")
            
            refresh_btn.click(
                fn=list_output_files,
                outputs=file_list_output
            )
            
            clear_btn.click(
                fn=clear_outputs,
                inputs=[clear_days],
                outputs=clear_status
            )
            
            # Auto-load file list on tab open
            app.load(fn=list_output_files, outputs=file_list_output)
    
    gr.Markdown("""
    ---
    ### 📚 Supported Formats
    **Input:** PDF, DOCX, DOC, PPTX, XLSX, HTML, MD, TXT  
    **Output:** Markdown (.md), HTML (.html), JSON (.json)
    
    ### 💡 Tips
    - Select your preferred output formats using the checkboxes above
    - Parsed documents are saved with timestamps in the `output/` directory
    - Multiple formats can be generated simultaneously
    - Use batch mode for processing multiple documents efficiently
    - Enable GPU acceleration for faster processing (requires GPU setup)
    - Watch the progress indicator during batch processing
    
    ### 🔗 Powered By
    - [Docling](https://github.com/docling-project/docling) - Document parsing library
    - [Docling-Parse](https://github.com/docling-project/docling-parse) - Enhanced parsing capabilities
    - [Gradio](https://www.gradio.app/) - Web interface framework
    """)


def launch_app(share=False, server_port=7860):
    """
    Launch the Gradio application.
    
    Args:
        share: Whether to create a public link
        server_port: Port to run the server on
    """
    # Ensure directories exist
    Path("input").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)
    
    logger.info(f"Launching Docling Parser UI on port {server_port}")
    
    app.launch(
        share=share,
        server_port=server_port,
        server_name="0.0.0.0",
        show_error=True
    )


if __name__ == "__main__":
    launch_app()

# Made with Bob
