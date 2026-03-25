"""
Docling Parser Module - Enhanced Version
Handles document parsing using the Docling library with support for:
- Batch and individual processing
- Multiple output formats (Markdown, HTML, JSON, Multimodal)
- Figure extraction
- Full page OCR with multiple OCR engines
- XBRL document conversion
- CSV file conversion
"""

import os
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Union, Callable
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    EasyOcrOptions,
    RapidOcrOptions,
    TesseractOcrOptions,
    OcrMacOptions
)
from docling_core.types.doc.base import ImageRefMode
from docling_core.types.doc.document import PictureItem, TableItem
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DoclingParser:
    """
    Enhanced parser class for processing documents using Docling library.
    Supports CPU/GPU modes, batch processing, multiple output formats,
    figure extraction, OCR, XBRL, and CSV conversion.
    """
    
    # OCR engine options
    OCR_ENGINES = {
        'none': 'No OCR',
        'rapidocr': 'RapidOCR (Fast & Accurate) - Recommended',
        'easyocr': 'EasyOCR (Deep Learning)',
        'tesseract': 'Tesseract OCR (Traditional)',
        'ocrmac': 'macOS Vision OCR (macOS only)'
    }
    
    def __init__(self, use_gpu: bool = False, output_dir: str = "output"):
        """
        Initialize the Docling parser.
        
        Args:
            use_gpu: Whether to use GPU acceleration (if available)
            output_dir: Directory to save parsed outputs
        """
        self.use_gpu = use_gpu
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for different output types
        self.figures_dir = self.output_dir / "figures"
        self.figures_dir.mkdir(exist_ok=True)
        
        # Initialize the document converter with default settings
        self.converter = DocumentConverter()
        
        logger.info(f"DoclingParser initialized (GPU: {use_gpu})")
    
    def _validate_ocr_engine(self, ocr_engine: str) -> str:
        """
        Validate and potentially fallback OCR engine selection.
        
        Args:
            ocr_engine: Requested OCR engine
            
        Returns:
            Validated OCR engine (may fallback to 'rapidocr' or 'none' if unavailable)
        """
        if ocr_engine == 'none':
            return ocr_engine
        
        if ocr_engine == 'rapidocr':
            # RapidOCR is included with Docling 2.74.0+
            logger.info("RapidOCR selected (built-in with Docling)")
            return ocr_engine
            
        if ocr_engine == 'easyocr':
            try:
                import easyocr
                # Just check if the module can be imported
                # Don't initialize Reader here as it downloads models
                logger.info("EasyOCR module found")
                return ocr_engine
            except ImportError as e:
                logger.warning(f"EasyOCR not installed: {e}. Falling back to RapidOCR.")
                return 'rapidocr'
            except Exception as e:
                logger.warning(f"EasyOCR error: {e}. Falling back to RapidOCR.")
                return 'rapidocr'
                
        elif ocr_engine == 'tesseract':
            try:
                import pytesseract
                # Test if Tesseract is available
                pytesseract.get_tesseract_version()
                logger.info("Tesseract OCR validation successful")
                return ocr_engine
            except Exception as e:
                logger.warning(f"Tesseract OCR not available: {e}. Falling back to RapidOCR.")
                return 'rapidocr'
                
        elif ocr_engine == 'ocrmac':
            import platform
            if platform.system() == 'Darwin':  # macOS
                logger.info("macOS Vision OCR selected")
                return ocr_engine
            else:
                logger.warning("macOS Vision OCR only available on macOS. Falling back to RapidOCR.")
                return 'rapidocr'
        
        logger.warning(f"Unknown OCR engine '{ocr_engine}'. Falling back to RapidOCR.")
        return 'rapidocr'
    
    def _configure_ocr_pipeline(self, ocr_engine: str = 'none', force_ocr: bool = False) -> PdfPipelineOptions:
        """
        Configure PDF pipeline with OCR options.
        
        Args:
            ocr_engine: OCR engine to use ('none', 'easyocr', 'tesseract', 'ocrmac')
            force_ocr: Force full page OCR even if text is extractable
            
        Returns:
            Configured PdfPipelineOptions
        """
        # Validate OCR engine availability
        validated_engine = self._validate_ocr_engine(ocr_engine)
        
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = (validated_engine != 'none')
        
        # Enable image generation for figures and pictures
        pipeline_options.generate_picture_images = True
        
        if validated_engine == 'rapidocr':
            pipeline_options.ocr_options = RapidOcrOptions(
                force_full_page_ocr=force_ocr
            )
        elif validated_engine == 'easyocr':
            pipeline_options.ocr_options = EasyOcrOptions(
                force_full_page_ocr=force_ocr,
                suppress_mps_warnings=True  # Suppress MPS warnings on macOS
            )
        elif validated_engine == 'tesseract':
            pipeline_options.ocr_options = TesseractOcrOptions(force_full_page_ocr=force_ocr)
        elif validated_engine == 'ocrmac':
            pipeline_options.ocr_options = OcrMacOptions(force_full_page_ocr=force_ocr)
        
        if validated_engine != ocr_engine:
            logger.info(f"OCR engine changed from '{ocr_engine}' to '{validated_engine}' due to availability")
        
        return pipeline_options
    
    def parse_document(self, 
                      file_path: Union[str, Path],
                      output_formats: Optional[List[str]] = None,
                      export_figures: bool = False,
                      export_multimodal: bool = False,
                      ocr_engine: str = 'none',
                      force_ocr: bool = False,
                      progress_callback: Optional[Callable[[str], None]] = None) -> Dict:
        """
        Parse a single document with enhanced features.
        
        Args:
            file_path: Path to the document file
            output_formats: List of output formats ['markdown', 'html', 'json', 'doctags']
            export_figures: Extract and save figures separately
            export_multimodal: Export with multimodal content (images embedded)
            ocr_engine: OCR engine to use ('none', 'easyocr', 'tesseract', 'ocrmac')
            force_ocr: Force full page OCR
            progress_callback: Optional callback function for progress updates
            
        Returns:
            Dictionary containing parsing results and metadata
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Default output formats
        if output_formats is None:
            output_formats = ['markdown', 'json']
        
        # Normalize format names
        output_formats = [fmt.lower() for fmt in output_formats]
        
        logger.info(f"Parsing document: {file_path.name}")
        if progress_callback:
            progress_callback(f"📄 Loading document: {file_path.name}")
        
        try:
            # Configure converter based on file type and options
            if file_path.suffix.lower() == '.pdf':
                pipeline_options = self._configure_ocr_pipeline(ocr_engine, force_ocr)
                converter = DocumentConverter(
                    format_options={
                        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
                    }
                )
            elif file_path.suffix.lower() == '.csv':
                # CSV files need special handling
                return self._parse_csv_file(file_path, output_formats, progress_callback)
            elif file_path.suffix.lower() in ['.xbrl', '.xml']:
                # XBRL files need special handling
                return self._parse_xbrl_file(file_path, output_formats, progress_callback)
            else:
                converter = self.converter
            
            # Convert the document
            if progress_callback:
                progress_callback(f"🔄 Converting document...")
            
            result = converter.convert(str(file_path))
            
            if progress_callback:
                progress_callback(f"✅ Document converted successfully")
            
            # Create timestamped output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{file_path.stem}_{timestamp}"
            
            outputs = {}
            figure_count = 0
            
            # Export figures if requested
            if export_figures:
                if progress_callback:
                    progress_callback(f"🖼️ Extracting figures...")
                
                figure_count = self._export_figures(result.document, output_filename)
                outputs['figures'] = str(self.figures_dir / output_filename)
                
                if progress_callback:
                    progress_callback(f"✅ Extracted {figure_count} figures")
            
            # Generate Markdown output
            if 'markdown' in output_formats:
                if progress_callback:
                    progress_callback(f"📝 Generating Markdown output...")
                
                if export_multimodal:
                    # Multimodal export with embedded images
                    markdown_content = result.document.export_to_markdown(
                        image_mode=ImageRefMode.EMBEDDED
                    )
                else:
                    markdown_content = result.document.export_to_markdown()
                
                markdown_path = self.output_dir / f"{output_filename}.md"
                
                with open(markdown_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                
                outputs['markdown'] = str(markdown_path)
                logger.info(f"Markdown saved: {markdown_path.name}")
            
            # Generate HTML output
            if 'html' in output_formats:
                if progress_callback:
                    progress_callback(f"🌐 Generating HTML output...")
                
                html_content = result.document.export_to_html()
                html_path = self.output_dir / f"{output_filename}.html"
                
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                outputs['html'] = str(html_path)
                logger.info(f"HTML saved: {html_path.name}")
            
            # Generate JSON output
            if 'json' in output_formats:
                if progress_callback:
                    progress_callback(f"🔧 Generating JSON output...")
                
                json_path = self.output_dir / f"{output_filename}.json"
                result.document.save_as_json(str(json_path))
                
                outputs['json'] = str(json_path)
                logger.info(f"JSON saved: {json_path.name}")
            
            # Generate DocTags output (document structure tags)
            if 'doctags' in output_formats:
                if progress_callback:
                    progress_callback(f"🏷️ Generating DocTags output...")
                
                doctags_content = result.document.export_to_document_tokens()
                doctags_path = self.output_dir / f"{output_filename}_doctags.txt"
                
                with open(doctags_path, 'w', encoding='utf-8') as f:
                    f.write(str(doctags_content))
                
                outputs['doctags'] = str(doctags_path)
                logger.info(f"DocTags saved: {doctags_path.name}")
            
            if progress_callback:
                progress_callback(f"✨ Processing complete!")
            
            logger.info(f"Successfully parsed: {file_path.name}")
            
            return {
                "status": "success",
                "input_file": str(file_path),
                "outputs": outputs,
                "timestamp": timestamp,
                "page_count": len(result.document.pages) if hasattr(result.document, 'pages') else 0,
                "formats": output_formats,
                "figure_count": figure_count,
                "ocr_engine": ocr_engine if ocr_engine != 'none' else None,
                "force_ocr": force_ocr
            }
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error parsing {file_path.name}: {error_msg}")
            
            if progress_callback:
                progress_callback(f"❌ Error: {error_msg}")
            
            return {
                "status": "error",
                "input_file": str(file_path),
                "error": error_msg,
                "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S")
            }
    
    def _export_figures(self, document, output_filename: str) -> int:
        """
        Export figures from document to separate files.
        
        Args:
            document: Docling document object
            output_filename: Base filename for outputs
            
        Returns:
            Number of figures exported
        """
        figure_dir = self.figures_dir / output_filename
        figure_dir.mkdir(exist_ok=True)
        
        figure_count = 0
        
        for element, _level in document.iterate_items():
            if isinstance(element, PictureItem):
                figure_count += 1
                
                # Get the image
                if element.image:
                    image_filename = figure_dir / f"figure_{figure_count}.png"
                    
                    # Save the image
                    pil_image = element.image.pil_image
                    if pil_image:
                        pil_image.save(image_filename)
                        logger.info(f"Saved figure: {image_filename.name}")
                    
                    # Save caption if available
                    if element.caption_text(document):
                        caption_filename = figure_dir / f"figure_{figure_count}_caption.txt"
                        with open(caption_filename, 'w', encoding='utf-8') as f:
                            f.write(element.caption_text(document))
        
        return figure_count
    
    def _parse_csv_file(self, file_path: Path, output_formats: List[str], 
                       progress_callback: Optional[Callable[[str], None]] = None) -> Dict:
        """
        Parse CSV file using pandas and convert to requested formats.
        
        Args:
            file_path: Path to CSV file
            output_formats: List of output formats
            progress_callback: Progress callback function
            
        Returns:
            Dictionary containing parsing results
        """
        try:
            import pandas as pd
            
            if progress_callback:
                progress_callback(f"📊 Reading CSV file...")
            
            # Read CSV file
            df = pd.read_csv(file_path)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{file_path.stem}_{timestamp}"
            outputs = {}
            
            # Generate Markdown table
            if 'markdown' in output_formats:
                if progress_callback:
                    progress_callback(f"📝 Converting to Markdown...")
                
                markdown_content = f"# {file_path.stem}\n\n"
                md_table = df.to_markdown(index=False)
                if md_table:
                    markdown_content += md_table
                
                markdown_path = self.output_dir / f"{output_filename}.md"
                with open(markdown_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                
                outputs['markdown'] = str(markdown_path)
            
            # Generate HTML table
            if 'html' in output_formats:
                if progress_callback:
                    progress_callback(f"🌐 Converting to HTML...")
                
                html_content = f"<html><head><title>{file_path.stem}</title></head><body>"
                html_content += f"<h1>{file_path.stem}</h1>"
                html_content += df.to_html(index=False)
                html_content += "</body></html>"
                
                html_path = self.output_dir / f"{output_filename}.html"
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                outputs['html'] = str(html_path)
            
            # Generate JSON
            if 'json' in output_formats:
                if progress_callback:
                    progress_callback(f"🔧 Converting to JSON...")
                
                json_path = self.output_dir / f"{output_filename}.json"
                df.to_json(json_path, orient='records', indent=2)
                
                outputs['json'] = str(json_path)
            
            return {
                "status": "success",
                "input_file": str(file_path),
                "outputs": outputs,
                "timestamp": timestamp,
                "row_count": len(df),
                "column_count": len(df.columns),
                "formats": output_formats
            }
            
        except Exception as e:
            return {
                "status": "error",
                "input_file": str(file_path),
                "error": str(e),
                "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S")
            }
    
    def _parse_xbrl_file(self, file_path: Path, output_formats: List[str],
                        progress_callback: Optional[Callable[[str], None]] = None) -> Dict:
        """
        Parse XBRL file and convert to requested formats.
        
        Args:
            file_path: Path to XBRL file
            output_formats: List of output formats
            progress_callback: Progress callback function
            
        Returns:
            Dictionary containing parsing results
        """
        try:
            try:
                from lxml import etree
            except ImportError:
                import xml.etree.ElementTree as etree
            
            if progress_callback:
                progress_callback(f"📋 Reading XBRL file...")
            
            # Parse XBRL XML
            tree = etree.parse(str(file_path))
            root = tree.getroot()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{file_path.stem}_{timestamp}"
            outputs = {}
            
            # Extract XBRL data
            xbrl_data = self._extract_xbrl_data(root)
            
            # Generate Markdown
            if 'markdown' in output_formats:
                if progress_callback:
                    progress_callback(f"📝 Converting to Markdown...")
                
                markdown_content = f"# XBRL Document: {file_path.stem}\n\n"
                markdown_content += self._xbrl_to_markdown(xbrl_data)
                
                markdown_path = self.output_dir / f"{output_filename}.md"
                with open(markdown_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                
                outputs['markdown'] = str(markdown_path)
            
            # Generate HTML
            if 'html' in output_formats:
                if progress_callback:
                    progress_callback(f"🌐 Converting to HTML...")
                
                html_content = f"<html><head><title>{file_path.stem}</title></head><body>"
                html_content += f"<h1>XBRL Document: {file_path.stem}</h1>"
                html_content += self._xbrl_to_html(xbrl_data)
                html_content += "</body></html>"
                
                html_path = self.output_dir / f"{output_filename}.html"
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                outputs['html'] = str(html_path)
            
            # Generate JSON
            if 'json' in output_formats:
                if progress_callback:
                    progress_callback(f"🔧 Converting to JSON...")
                
                json_path = self.output_dir / f"{output_filename}.json"
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(xbrl_data, f, indent=2)
                
                outputs['json'] = str(json_path)
            
            return {
                "status": "success",
                "input_file": str(file_path),
                "outputs": outputs,
                "timestamp": timestamp,
                "formats": output_formats
            }
            
        except Exception as e:
            return {
                "status": "error",
                "input_file": str(file_path),
                "error": str(e),
                "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S")
            }
    
    def _extract_xbrl_data(self, root) -> Dict:
        """Extract data from XBRL XML root."""
        data = {
            "facts": [],
            "contexts": [],
            "units": []
        }
        
        # Extract facts (simplified)
        for elem in root.iter():
            if elem.text and elem.text.strip():
                data["facts"].append({
                    "tag": elem.tag,
                    "value": elem.text.strip(),
                    "attributes": dict(elem.attrib)
                })
        
        return data
    
    def _xbrl_to_markdown(self, xbrl_data: Dict) -> str:
        """Convert XBRL data to Markdown format."""
        md = "## XBRL Facts\n\n"
        for fact in xbrl_data.get("facts", [])[:50]:  # Limit to first 50
            md += f"- **{fact['tag']}**: {fact['value']}\n"
        return md
    
    def _xbrl_to_html(self, xbrl_data: Dict) -> str:
        """Convert XBRL data to HTML format."""
        html = "<h2>XBRL Facts</h2><ul>"
        for fact in xbrl_data.get("facts", [])[:50]:  # Limit to first 50
            html += f"<li><strong>{fact['tag']}</strong>: {fact['value']}</li>"
        html += "</ul>"
        return html
    
    def parse_batch(self, 
                   input_dir: Union[str, Path],
                   output_formats: Optional[List[str]] = None,
                   export_figures: bool = False,
                   export_multimodal: bool = False,
                   ocr_engine: str = 'none',
                   force_ocr: bool = False,
                   file_extensions: Optional[List[str]] = None,
                   progress_callback: Optional[Callable[[str, int, int], None]] = None) -> List[Dict]:
        """
        Parse all documents in a directory with enhanced features.
        
        Args:
            input_dir: Directory containing documents to parse
            output_formats: List of output formats
            export_figures: Extract and save figures separately
            export_multimodal: Export with multimodal content
            ocr_engine: OCR engine to use
            force_ocr: Force full page OCR
            file_extensions: List of file extensions to process
            progress_callback: Optional callback for progress updates
            
        Returns:
            List of dictionaries containing parsing results for each file
        """
        input_dir = Path(input_dir)
        
        if not input_dir.exists():
            raise FileNotFoundError(f"Input directory not found: {input_dir}")
        
        if file_extensions is None:
            file_extensions = ['.pdf', '.docx', '.doc', '.pptx', '.xlsx', '.html', '.md', '.csv', '.xbrl', '.xml']
        
        if output_formats is None:
            output_formats = ['markdown', 'json']
        
        # Find all matching files
        files_to_process = []
        for ext in file_extensions:
            files_to_process.extend(input_dir.glob(f"*{ext}"))
            files_to_process.extend(input_dir.glob(f"*{ext.upper()}"))
        
        total_files = len(files_to_process)
        logger.info(f"Found {total_files} files to process in {input_dir}")
        
        if progress_callback:
            progress_callback(f"📁 Found {total_files} files to process", 0, total_files)
        
        results = []
        for i, file_path in enumerate(files_to_process, 1):
            if progress_callback:
                progress_callback(f"Processing file {i}/{total_files}: {file_path.name}", i-1, total_files)
            
            # Create a file-specific progress callback
            def file_progress(msg):
                if progress_callback:
                    progress_callback(f"[{i}/{total_files}] {msg}", i-1, total_files)
            
            result = self.parse_document(
                file_path, 
                output_formats, 
                export_figures=export_figures,
                export_multimodal=export_multimodal,
                ocr_engine=ocr_engine,
                force_ocr=force_ocr,
                progress_callback=file_progress
            )
            results.append(result)
            
            if progress_callback:
                status = "✅" if result["status"] == "success" else "❌"
                progress_callback(f"{status} Completed: {file_path.name}", i, total_files)
        
        # Generate summary
        successful = sum(1 for r in results if r["status"] == "success")
        failed = total_files - successful
        
        logger.info(f"Batch processing complete: {successful} successful, {failed} failed")
        
        if progress_callback:
            progress_callback(f"🎉 Batch complete: {successful} successful, {failed} failed", total_files, total_files)
        
        return results
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported document formats."""
        return ['.pdf', '.docx', '.doc', '.pptx', '.xlsx', '.html', '.md', '.txt', '.csv', '.xbrl', '.xml']
    
    def get_output_formats(self) -> List[str]:
        """Get list of supported output formats."""
        return ['markdown', 'html', 'json', 'doctags']
    
    def get_ocr_engines(self) -> Dict[str, str]:
        """Get available OCR engines."""
        return self.OCR_ENGINES.copy()
    
    def clear_output_directory(self, older_than_days: Optional[int] = None):
        """
        Clear old files from the output directory.
        
        Args:
            older_than_days: Only delete files older than this many days.
                           If None, deletes all files.
        """
        if older_than_days is None:
            # Delete all files
            for file_path in self.output_dir.glob("*"):
                if file_path.is_file():
                    file_path.unlink()
                    logger.info(f"Deleted: {file_path.name}")
        else:
            # Delete files older than specified days
            cutoff_time = datetime.now().timestamp() - (older_than_days * 86400)
            for file_path in self.output_dir.glob("*"):
                if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
                    logger.info(f"Deleted old file: {file_path.name}")


def main():
    """Example usage of the enhanced DoclingParser class."""
    parser = DoclingParser(use_gpu=False, output_dir="output")
    
    # Example: Parse with OCR and figure extraction
    def progress_update(message):
        print(f"Progress: {message}")
    
    # Batch processing with all features
    def batch_progress(message, current, total):
        percentage = (current / total * 100) if total > 0 else 0
        print(f"[{percentage:.1f}%] {message}")
    
    results = parser.parse_batch(
        "input",
        output_formats=['markdown', 'html', 'json'],
        export_figures=True,
        export_multimodal=False,
        ocr_engine='easyocr',
        force_ocr=False,
        progress_callback=batch_progress
    )
    
    # Print summary
    print("\n" + "="*50)
    print("BATCH PROCESSING SUMMARY")
    print("="*50)
    for result in results:
        status_icon = "✓" if result["status"] == "success" else "✗"
        file_name = Path(result['input_file']).name
        if result["status"] == "success":
            formats = ", ".join(result.get('formats', []))
            figures = result.get('figure_count', 0)
            print(f"{status_icon} {file_name}: {formats} ({figures} figures)")
        else:
            print(f"{status_icon} {file_name}: {result.get('error', 'Unknown error')}")
    print("="*50)


if __name__ == "__main__":
    main()

# Made with Bob
