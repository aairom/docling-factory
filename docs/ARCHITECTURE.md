# Architecture Documentation - Enhanced Edition

This document provides a detailed overview of the enhanced Docling Document Parser application architecture with advanced features.

## System Overview

```mermaid
graph TB
    subgraph "User Layer"
        USER[User/Browser]
    end
    
    subgraph "Presentation Layer"
        GRADIO[Gradio Web Interface<br/>Port: 7860<br/>Enhanced UI]
    end
    
    subgraph "Application Layer"
        APP[app.py<br/>UI Logic & Routing<br/>Feature Controls]
        PARSER[docling_parser.py<br/>Enhanced Parser Module]
    end
    
    subgraph "Processing Layer"
        DOCLING[Docling Library<br/>Document Conversion]
        OCR_EASY[EasyOCR<br/>Deep Learning]
        OCR_TESS[Tesseract OCR<br/>Traditional]
        OCR_MAC[macOS Vision<br/>Native]
        TABLE[Table Detection]
        LAYOUT[Layout Analysis]
        FIG_EXT[Figure Extraction]
        MULTI[Multimodal Export]
    end
    
    subgraph "Format Handlers"
        CSV_H[CSV Handler]
        XBRL_H[XBRL Handler]
        PDF_H[PDF Handler]
    end
    
    subgraph "Hardware Layer"
        CPU[CPU Processing]
        GPU[GPU Acceleration<br/>Optional]
    end
    
    subgraph "Storage Layer"
        INPUT[input/<br/>Source Documents]
        OUTPUT[output/<br/>Parsed Results]
        FIGURES[output/figures/<br/>Extracted Images]
        LOGS[logs/<br/>Application Logs]
    end
    
    USER <-->|HTTP| GRADIO
    GRADIO <--> APP
    APP <--> PARSER
    PARSER <--> DOCLING
    PARSER <--> CSV_H
    PARSER <--> XBRL_H
    PARSER <--> PDF_H
    DOCLING --> OCR_EASY
    DOCLING --> OCR_TESS
    DOCLING --> OCR_MAC
    DOCLING --> TABLE
    DOCLING --> LAYOUT
    DOCLING --> FIG_EXT
    DOCLING --> MULTI
    DOCLING <--> CPU
    DOCLING -.->|Optional| GPU
    PARSER --> INPUT
    PARSER --> OUTPUT
    FIG_EXT --> FIGURES
    APP --> LOGS
    
    style USER fill:#e1f5ff
    style GRADIO fill:#fff3e0
    style APP fill:#fff3e0
    style PARSER fill:#fff3e0
    style DOCLING fill:#f3e5f5
    style OCR_EASY fill:#e8f5e9
    style OCR_TESS fill:#e8f5e9
    style OCR_MAC fill:#e8f5e9
    style FIG_EXT fill:#fff9c4
    style MULTI fill:#fff9c4
    style CSV_H fill:#f3e5f5
    style XBRL_H fill:#f3e5f5
    style GPU fill:#f3e5f5,stroke-dasharray: 5 5
    style INPUT fill:#e8f5e9
    style OUTPUT fill:#e8f5e9
    style FIGURES fill:#fff9c4
    style LOGS fill:#e8f5e9
```

## Component Details

### 1. Presentation Layer

#### Gradio Web Interface
- **Technology**: Gradio 4.0+
- **Port**: 7860 (configurable)
- **Features**:
  - Three main tabs: Individual Upload, Batch Processing, Output Management
  - Real-time progress tracking
  - File upload handling
  - Result visualization

### 2. Application Layer

#### app.py (Main Application - Enhanced)
- **Purpose**: UI logic and user interaction handling with advanced features
- **Key Functions**:
  - `parse_single_file()`: Handle individual file uploads with all features
  - `parse_batch_files()`: Coordinate batch processing with progress tracking
  - `list_output_files()`: Manage output directory
  - `clear_outputs()`: Clean old files
  - `launch_app()`: Application entry point
- **New Features**:
  - Output format selection (Markdown, HTML, JSON, DocTags)
  - Figure extraction toggle
  - Multimodal export toggle
  - OCR engine selection dropdown
  - Force OCR checkbox

#### docling_parser.py (Enhanced Core Parser)
- **Purpose**: Advanced document parsing and conversion logic
- **Key Classes**:
  - `DoclingParser`: Enhanced main parser class
- **Key Methods**:
  - `parse_document()`: Parse with OCR, figures, multimodal support
  - `parse_batch()`: Batch processing with all features
  - `_configure_ocr_pipeline()`: Configure OCR settings
  - `_export_figures()`: Extract and save figures
  - `_parse_csv_file()`: Handle CSV conversion
  - `_parse_xbrl_file()`: Handle XBRL conversion
  - `get_supported_formats()`: List all supported formats
  - `get_ocr_engines()`: List available OCR engines
  - `clear_output_directory()`: Cleanup utility

### 3. Processing Layer

#### Docling Library
- **Version**: 2.0+
- **Capabilities**:
  - Multi-format document conversion
  - OCR (Optical Character Recognition)
  - Table structure detection
  - Layout analysis
  - Metadata extraction

### 4. Hardware Layer

#### CPU Processing
- **Default Mode**: Always available
- **Performance**: Suitable for most documents
- **Memory**: Depends on document size

#### GPU Acceleration (Optional)
- **Requirements**: CUDA-compatible GPU
- **Performance**: 3-5x faster than CPU
- **Libraries**: PyTorch, CUDA toolkit

## Data Flow

### Individual File Processing

```mermaid
sequenceDiagram
    participant U as User
    participant G as Gradio UI
    participant A as app.py
    participant P as DoclingParser
    participant D as Docling
    participant F as File System
    
    U->>G: Upload File
    G->>A: file_upload_event()
    A->>P: parse_document(file_path)
    P->>F: Read file
    F-->>P: File data
    P->>D: convert(file)
    D->>D: OCR + Analysis
    D-->>P: Document object
    P->>P: Extract markdown
    P->>P: Extract JSON
    P->>F: Save outputs
    F-->>P: Success
    P-->>A: Result object
    A->>G: Update UI
    G-->>U: Display results
```

### Batch Processing

```mermaid
sequenceDiagram
    participant U as User
    participant G as Gradio UI
    participant A as app.py
    participant P as DoclingParser
    participant D as Docling
    participant F as File System
    
    U->>G: Click "Process Batch"
    G->>A: batch_process_event()
    A->>P: parse_batch(input_dir)
    P->>F: List files in input/
    F-->>P: File list
    
    loop For each file
        P->>D: convert(file)
        D-->>P: Document object
        P->>F: Save outputs
        P->>G: Update progress
    end
    
    P-->>A: Results array
    A->>G: Display summary
    G-->>U: Show results
```

## File Structure

```
edf-docling/
├── app.py                      # Main Gradio application
├── docling_parser.py           # Core parsing module
├── requirements.txt            # CPU dependencies
├── requirements-gpu.txt        # GPU dependencies
├── README.md                   # Main documentation
├── .gitignore                 # Git ignore rules
│
├── docs/                      # Documentation
│   ├── README.md              # Detailed docs
│   ├── QUICKSTART.md          # Quick start guide
│   ├── workflows.md           # Workflow diagrams
│   └── ARCHITECTURE.md        # This file
│
├── scripts/                   # Automation scripts
│   ├── setup.sh               # Environment setup
│   ├── launch.sh              # Start application
│   ├── stop.sh                # Stop application
│   ├── status.sh              # Check status
│   └── test.sh                # Run tests
│
├── input/                     # Input documents
│   └── README.md              # Input directory guide
│
├── output/                    # Parsed outputs
│   ├── *.md                   # Markdown outputs
│   └── *.json                 # JSON outputs
│
└── logs/                      # Application logs
    └── app.log                # Main log file
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DOCLING_PORT` | 7860 | Web server port |
| `DOCLING_USE_GPU` | false | Enable GPU acceleration |
| `DOCLING_SHARE` | false | Create public share link |
| `DOCLING_INPUT_DIR` | ./input | Input directory path |
| `DOCLING_OUTPUT_DIR` | ./output | Output directory path |

### Parser Configuration

```python
parser = DoclingParser(
    use_gpu=False,           # GPU acceleration
    output_dir="output"      # Output directory
)
```

### Pipeline Options

```python
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = True              # Enable OCR
pipeline_options.do_table_structure = True  # Enable table detection
```

## Performance Considerations

### CPU Mode
- **Pros**: Works everywhere, no special hardware
- **Cons**: Slower processing (1-2 pages/second)
- **Best for**: Small batches, occasional use

### GPU Mode
- **Pros**: 3-5x faster processing
- **Cons**: Requires CUDA GPU, more memory
- **Best for**: Large batches, frequent use

### Memory Usage

| Document Type | Typical Memory |
|---------------|----------------|
| Small PDF (<10 pages) | 100-200 MB |
| Medium PDF (10-50 pages) | 200-500 MB |
| Large PDF (>50 pages) | 500 MB - 2 GB |
| DOCX/PPTX | 50-200 MB |

## Security Considerations

1. **File Upload**: Only processes files in designated directories
2. **Output Isolation**: Outputs are timestamped to prevent overwrites
3. **No External Access**: By default, only accessible on localhost
4. **Process Isolation**: Runs in virtual environment

## Scalability

### Horizontal Scaling
- Run multiple instances on different ports
- Use load balancer for distribution
- Shared storage for input/output

### Vertical Scaling
- Increase CPU cores for parallel processing
- Add GPU for faster processing
- Increase RAM for larger documents

## Monitoring

### Application Logs
- Location: `logs/app.log`
- Format: Timestamped entries with log levels
- Rotation: Manual (use output management)

### Process Monitoring
```bash
./scripts/status.sh  # Check application status
tail -f logs/app.log # Watch logs in real-time
```

## Deployment Options

### Local Development
```bash
./scripts/launch.sh
```

### Production (Background)
```bash
./scripts/launch.sh --detached --port 8080
```

### Docker (Future Enhancement)
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## Error Handling

### Application Level
- Try-catch blocks for all operations
- Graceful degradation (GPU → CPU fallback)
- User-friendly error messages

### File Level
- Validation before processing
- Partial success in batch mode
- Detailed error logging

## Future Enhancements

1. **API Endpoint**: REST API for programmatic access
2. **Authentication**: User login and access control
3. **Cloud Storage**: S3/Azure Blob integration
4. **Webhooks**: Notification on completion
5. **Docker Support**: Containerized deployment
6. **Kubernetes**: Orchestrated scaling
7. **Database**: Store processing history
8. **Analytics**: Usage statistics and insights

## Dependencies

### Core Dependencies
- Python 3.8+
- Docling 2.0+
- Gradio 4.0+

### Optional Dependencies
- PyTorch (GPU support)
- CUDA Toolkit (GPU support)

### System Dependencies
- bash (for scripts)
- Standard Unix utilities (ps, kill, lsof)

## Testing Strategy

### Unit Tests
- Parser module functions
- File handling operations
- Configuration management

### Integration Tests
- End-to-end document processing
- Batch processing workflows
- Error handling scenarios

### Performance Tests
- Large document processing
- Batch processing speed
- Memory usage profiling

## Maintenance

### Regular Tasks
1. Clear old outputs: `./scripts/stop.sh` → Output Management
2. Check logs: `tail -f logs/app.log`
3. Update dependencies: `pip install --upgrade -r requirements.txt`

### Troubleshooting
1. Check status: `./scripts/status.sh`
2. Review logs: `logs/app.log`
3. Run tests: `./scripts/test.sh`
4. Restart: `./scripts/stop.sh && ./scripts/launch.sh`

## Support

For issues or questions:
- Check documentation: `docs/README.md`
- Review workflows: `docs/workflows.md`
- Docling issues: https://github.com/docling-project/docling