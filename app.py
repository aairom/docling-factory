"""
Docling Document Parser - Enhanced Gradio UI Application
A comprehensive interface for parsing documents using Docling library with:
- Multiple output formats (Markdown, HTML, JSON, DocTags)
- Multimodal export with embedded images
- Figure extraction
- Full page OCR with multiple engine options
- XBRL document conversion
- CSV file conversion
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


def parse_single_file(file, use_gpu, markdown_check, html_check, json_check, doctags_check,
                     export_figures, export_multimodal, ocr_engine, force_ocr):
    """
    Parse a single uploaded file with selected options.
    
    Args:
        file: Uploaded file object from Gradio
        use_gpu: Boolean indicating whether to use GPU
        markdown_check: Boolean for Markdown output
        html_check: Boolean for HTML output
        json_check: Boolean for JSON output
        doctags_check: Boolean for DocTags output
        export_figures: Boolean to extract figures
        export_multimodal: Boolean for multimodal export
        ocr_engine: OCR engine selection
        force_ocr: Boolean to force full page OCR
        
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
    if doctags_check:
        output_formats.append('doctags')
    
    if not output_formats:
        return "⚠️ Please select at least one output format", "", "", "", ""
    
    try:
        # Initialize parser if needed
        if parser is None or parser.use_gpu != use_gpu:
            initialize_parser(use_gpu)
        
        progress_messages = []
        
        def progress_callback(msg):
            progress_messages.append(msg)
        
        # Parse the document with all options
        result = parser.parse_document(
            file.name, 
            output_formats,
            export_figures=export_figures,
            export_multimodal=export_multimodal,
            ocr_engine=ocr_engine,
            force_ocr=force_ocr,
            progress_callback=progress_callback
        )
        
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
"""
            
            if result.get('figure_count', 0) > 0:
                status_msg += f"- **Figures Extracted:** {result['figure_count']}\n"
            
            if result.get('ocr_engine'):
                status_msg += f"- **OCR Engine:** {result['ocr_engine']}\n"
            
            if result.get('force_ocr'):
                status_msg += f"- **Full Page OCR:** Enabled\n"
            
            status_msg += "\n**Generated Files:**\n"
            for fmt, path in result['outputs'].items():
                status_msg += f"\n- **{fmt.upper()}:** `{path}`"
            
            return status_msg, markdown_content, html_content, json_content, progress_text
        else:
            error_msg = f"❌ **Error parsing document:**\n\n{result['error']}"
            return error_msg, "", "", "", progress_text
            
    except Exception as e:
        logger.error(f"Error in parse_single_file: {str(e)}")
        return f"❌ **Error:** {str(e)}", "", "", "", ""


def parse_batch_files(use_gpu, markdown_check, html_check, json_check, doctags_check,
                     export_figures, export_multimodal, ocr_engine, force_ocr, progress=gr.Progress()):
    """
    Parse all files in the input directory with progress tracking.
    
    Args:
        use_gpu: Boolean indicating whether to use GPU
        markdown_check: Boolean for Markdown output
        html_check: Boolean for HTML output
        json_check: Boolean for JSON output
        doctags_check: Boolean for DocTags output
        export_figures: Boolean to extract figures
        export_multimodal: Boolean for multimodal export
        ocr_engine: OCR engine selection
        force_ocr: Boolean to force full page OCR
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
    if doctags_check:
        output_formats.append('doctags')
    
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
        
        # Process files with all options
        results = parser.parse_batch(
            input_dir, 
            output_formats,
            export_figures=export_figures,
            export_multimodal=export_multimodal,
            ocr_engine=ocr_engine,
            force_ocr=force_ocr,
            progress_callback=progress_callback
        )
        
        # Generate summary
        successful = [r for r in results if r["status"] == "success"]
        failed = [r for r in results if r["status"] == "error"]
        
        total_figures = sum(r.get('figure_count', 0) for r in successful)
        
        summary = f"""
## 📊 Batch Processing Complete

### Summary
- **Total Files:** {len(results)}
- **Successful:** {len(successful)} ✅
- **Failed:** {len(failed)} ❌
- **Output Formats:** {', '.join(output_formats)}
- **Figures Extracted:** {total_figures}
"""
        
        if ocr_engine != 'none':
            summary += f"- **OCR Engine:** {ocr_engine}\n"
        
        if force_ocr:
            summary += f"- **Full Page OCR:** Enabled\n"
        
        summary += "\n### Processed Files\n"
        
        for result in results:
            status_icon = "✅" if result["status"] == "success" else "❌"
            file_name = Path(result['input_file']).name
            summary += f"\n{status_icon} **{file_name}**"
            
            if result["status"] == "success":
                summary += f" - {result.get('page_count', 'N/A')} pages"
                formats_list = ', '.join(result.get('formats', []))
                summary += f" ({formats_list})"
                if result.get('figure_count', 0) > 0:
                    summary += f" - {result['figure_count']} figures"
            else:
                summary += f" - Error: {result.get('error', 'Unknown error')}"
        
        summary += f"\n\n### Output Location\nAll parsed documents are saved in the `output/` directory with timestamps."
        if total_figures > 0:
            summary += f"\nFigures are saved in `output/figures/` subdirectories."
        
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


# Create the enhanced Gradio interface
with gr.Blocks(title="Docling Document Parser - Enhanced", theme=gr.themes.Soft()) as app:
    gr.Markdown("""
    # 📄 Docling Document Parser - Enhanced Edition
    
    Parse documents with advanced features including **multimodal export**, **figure extraction**, 
    **OCR support**, **XBRL conversion**, and **CSV processing**.
    
    Supports PDF, DOCX, PPTX, XLSX, HTML, CSV, XBRL, and more with multiple output formats.
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
            doctags_check = gr.Checkbox(label="DocTags (.txt)", value=False, 
                                       info="Document structure tags")
        
        # Advanced features
        gr.Markdown("### 🚀 Advanced Features")
        with gr.Row():
            export_figures = gr.Checkbox(
                label="Extract Figures",
                value=False,
                info="Save images and figures separately"
            )
            export_multimodal = gr.Checkbox(
                label="Multimodal Export",
                value=False,
                info="Embed images in Markdown output"
            )
        
        # OCR settings
        gr.Markdown("### 🔍 OCR Settings")
        with gr.Row():
            ocr_engine = gr.Dropdown(
                choices=[
                    ("No OCR", "none"),
                    ("EasyOCR (Deep Learning)", "easyocr"),
                    ("Tesseract OCR (Traditional)", "tesseract"),
                    ("macOS Vision OCR", "ocrmac")
                ],
                value="none",
                label="OCR Engine",
                info="Select OCR engine for text extraction"
            )
            force_ocr = gr.Checkbox(
                label="Force Full Page OCR",
                value=False,
                info="Apply OCR even if text is extractable"
            )
    
    with gr.Tabs() as tabs:
        # Tab 1: Individual Upload
        with gr.Tab("📤 Individual Upload"):
            gr.Markdown("Upload a single document to parse it immediately with all selected features.")
            
            with gr.Row():
                with gr.Column(scale=1):
                    file_input = gr.File(
                        label="Upload Document",
                        file_types=[".pdf", ".docx", ".doc", ".pptx", ".xlsx", ".html", ".md", ".txt", ".csv", ".xbrl", ".xml"]
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
                inputs=[file_input, gpu_toggle, markdown_check, html_check, json_check, doctags_check,
                       export_figures, export_multimodal, ocr_engine, force_ocr],
                outputs=[status_output, markdown_output, html_output, json_output, progress_output]
            )
        
        # Tab 2: Batch Processing
        with gr.Tab("📦 Batch Processing"):
            gr.Markdown("""
            Process all documents in the `input/` directory at once with all selected features.
            
            **Instructions:**
            1. Place your documents in the `input/` folder
            2. Configure settings above (output formats, OCR, figure extraction, etc.)
            3. Click the "Process Batch" button
            4. Check the `output/` folder for results
            """)
            
            batch_btn = gr.Button("🚀 Process Batch", variant="primary", size="lg")
            batch_output = gr.Markdown(label="Batch Processing Results")
            
            batch_btn.click(
                fn=parse_batch_files,
                inputs=[gpu_toggle, markdown_check, html_check, json_check, doctags_check,
                       export_figures, export_multimodal, ocr_engine, force_ocr],
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
    **Input:** PDF, DOCX, DOC, PPTX, XLSX, HTML, MD, TXT, CSV, XBRL, XML  
    **Output:** Markdown (.md), HTML (.html), JSON (.json), DocTags (.txt)
    
    ### 🎯 Features
    - **Multiple Output Formats:** Generate Markdown, HTML, JSON, and DocTags simultaneously
    - **Figure Extraction:** Extract and save images/figures separately
    - **Multimodal Export:** Embed images directly in Markdown output
    - **OCR Support:** Choose from EasyOCR, Tesseract, or macOS Vision OCR
    - **Force Full Page OCR:** Apply OCR even when text is extractable
    - **XBRL Conversion:** Parse XBRL financial documents
    - **CSV Processing:** Convert CSV files to multiple formats
    - **Batch Processing:** Process multiple documents efficiently
    - **GPU Acceleration:** Faster processing with CUDA-compatible GPUs
    
    ### 💡 Tips
    - **OCR Engines:**
      - **EasyOCR:** Best for multilingual documents, uses deep learning
      - **Tesseract:** Traditional OCR, requires separate installation
      - **macOS Vision:** Native macOS OCR (macOS only)
    - **Figure Extraction:** Saves images in `output/figures/` subdirectories
    - **Multimodal Export:** Embeds images as base64 in Markdown
    - **Force OCR:** Useful for scanned documents or poor quality PDFs
    - **CSV Files:** Automatically converted to tables in selected formats
    - **XBRL Files:** Financial data extracted and formatted
    
    ### 🔗 Powered By
    - [Docling](https://github.com/docling-project/docling) - Document parsing library
    - [Docling-Parse](https://github.com/docling-project/docling-parse) - Enhanced parsing
    - [Gradio](https://www.gradio.app/) - Web interface framework
    - [EasyOCR](https://github.com/JaidedAI/EasyOCR) - Deep learning OCR
    - [Tesseract](https://github.com/tesseract-ocr/tesseract) - Traditional OCR
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
    Path("output/figures").mkdir(exist_ok=True)
    
    logger.info(f"Launching Enhanced Docling Parser UI on port {server_port}")
    
    app.launch(
        share=share,
        server_port=server_port,
        server_name="0.0.0.0",
        show_error=True
    )


if __name__ == "__main__":
    launch_app()

# Made with Bob
