"""
Docling Parser Module
Handles document parsing using the Docling library with support for batch and individual processing.
Enhanced with docling-parse integration, multiple output formats, and progress tracking.
"""

import os
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Union, Callable
from docling.document_converter import DocumentConverter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DoclingParser:
    """
    A parser class for processing documents using Docling library.
    Supports both CPU and GPU modes, batch processing, individual file processing,
    and multiple output formats (Markdown, HTML, JSON).
    """
    
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
        
        # Initialize the document converter with default settings
        self.converter = DocumentConverter()
        
        logger.info(f"DoclingParser initialized (GPU: {use_gpu})")
    
    def parse_document(self, 
                      file_path: Union[str, Path],
                      output_formats: Optional[List[str]] = None,
                      progress_callback: Optional[Callable[[str], None]] = None) -> Dict:
        """
        Parse a single document with support for multiple output formats.
        
        Args:
            file_path: Path to the document file
            output_formats: List of output formats ['markdown', 'html', 'json']
                          If None, defaults to ['markdown', 'json']
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
            # Convert the document
            if progress_callback:
                progress_callback(f"🔄 Converting document...")
            
            result = self.converter.convert(str(file_path))
            
            if progress_callback:
                progress_callback(f"✅ Document converted successfully")
            
            # Create timestamped output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{file_path.stem}_{timestamp}"
            
            outputs = {}
            
            # Generate Markdown output
            if 'markdown' in output_formats:
                if progress_callback:
                    progress_callback(f"📝 Generating Markdown output...")
                
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
            
            if progress_callback:
                progress_callback(f"✨ Processing complete!")
            
            logger.info(f"Successfully parsed: {file_path.name}")
            
            return {
                "status": "success",
                "input_file": str(file_path),
                "outputs": outputs,
                "timestamp": timestamp,
                "page_count": len(result.document.pages) if hasattr(result.document, 'pages') else 0,
                "formats": output_formats
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
    
    def parse_batch(self, 
                   input_dir: Union[str, Path],
                   output_formats: Optional[List[str]] = None,
                   file_extensions: Optional[List[str]] = None,
                   progress_callback: Optional[Callable[[str, int, int], None]] = None) -> List[Dict]:
        """
        Parse all documents in a directory with progress tracking.
        
        Args:
            input_dir: Directory containing documents to parse
            output_formats: List of output formats ['markdown', 'html', 'json']
            file_extensions: List of file extensions to process
            progress_callback: Optional callback function for progress updates
                             Receives (message, current_file_index, total_files)
            
        Returns:
            List of dictionaries containing parsing results for each file
        """
        input_dir = Path(input_dir)
        
        if not input_dir.exists():
            raise FileNotFoundError(f"Input directory not found: {input_dir}")
        
        if file_extensions is None:
            file_extensions = ['.pdf', '.docx', '.doc', '.pptx', '.xlsx', '.html', '.md']
        
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
            
            result = self.parse_document(file_path, output_formats, file_progress)
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
        """
        Get list of supported document formats.
        
        Returns:
            List of supported file extensions
        """
        return ['.pdf', '.docx', '.doc', '.pptx', '.xlsx', '.html', '.md', '.txt']
    
    def get_output_formats(self) -> List[str]:
        """
        Get list of supported output formats.
        
        Returns:
            List of supported output formats
        """
        return ['markdown', 'html', 'json']
    
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
    """
    Example usage of the DoclingParser class with enhanced features.
    """
    # Initialize parser
    parser = DoclingParser(use_gpu=False, output_dir="output")
    
    # Example 1: Parse a single document with multiple formats
    def progress_update(message):
        print(f"Progress: {message}")
    
    # result = parser.parse_document(
    #     "input/sample.pdf", 
    #     output_formats=['markdown', 'html', 'json'],
    #     progress_callback=progress_update
    # )
    # print(result)
    
    # Example 2: Parse all documents in a directory with progress
    def batch_progress(message, current, total):
        percentage = (current / total * 100) if total > 0 else 0
        print(f"[{percentage:.1f}%] {message}")
    
    results = parser.parse_batch(
        "input",
        output_formats=['markdown', 'html', 'json'],
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
            print(f"{status_icon} {file_name}: {result['status']} ({formats})")
        else:
            print(f"{status_icon} {file_name}: {result['status']} - {result.get('error', 'Unknown error')}")
    print("="*50)


if __name__ == "__main__":
    main()

# Made with Bob
