# 🚀 Quick Start Guide - Enhanced Edition

Get started with **Docling Factory Enhanced** in 3 simple steps!

## Step 1: Setup (One-time)

Run the setup script to install dependencies:

```bash
./scripts/setup.sh
```

For GPU support (requires CUDA):
```bash
./scripts/setup.sh --gpu
```

This will:
- Create a Python virtual environment
- Install all required dependencies (including OCR engines)
- Set up project directories

**Note:** For OCR support:
- **EasyOCR**: Installed automatically
- **Tesseract**: Requires separate installation
  - macOS: `brew install tesseract`
  - Ubuntu: `apt-get install tesseract-ocr`
  - Windows: Download from [Tesseract Wiki](https://github.com/UB-Mannheim/tesseract/wiki)

## Step 2: Start the Application

```bash
./scripts/launch.sh
```

The application will start and be available at: **http://localhost:7860**

### Advanced Options

```bash
# Run in background (detached mode)
./scripts/launch.sh --detached

# Use custom port
./scripts/launch.sh --port 8080

# Enable GPU acceleration
./scripts/launch.sh --gpu

# Combine options
./scripts/launch.sh --detached --port 8080 --gpu
```

## Step 3: Parse Documents

### Option A: Individual Upload with Advanced Features

1. Open http://localhost:7860 in your browser
2. **Configure Global Settings:**
   - **Output formats**: Markdown, HTML, JSON, DocTags
   - **Advanced Features**:
     - ✅ Extract Figures - Save images separately
     - ✅ Multimodal Export - Embed images in Markdown
   - **OCR Settings**:
     - Select OCR engine (EasyOCR, Tesseract, macOS Vision, or None)
     - ✅ Force Full Page OCR - For scanned documents
3. Go to the **"📤 Individual Upload"** tab
4. Click **"Upload Document"**
5. Select your file (PDF, DOCX, PPTX, CSV, XBRL, etc.)
6. Click **"🚀 Parse Document"**
7. **Watch real-time progress** including figure extraction and OCR
8. View results in separate tabs for each format!

### Option B: Batch Processing with All Features

1. Copy your documents to the `input/` folder
2. Open http://localhost:7860 in your browser
3. **Configure settings** (formats, OCR, figure extraction)
4. Go to the **"📦 Batch Processing"** tab
5. Click **"🚀 Process Batch"**
6. **Monitor progress** showing file processing, figure extraction, and OCR
7. All documents are processed with selected features!

Results are saved in the `output/` folder:
- Documents in selected formats with timestamps
- Figures in `output/figures/` subdirectories

## 📊 Examples

### Example 1: Basic Batch Processing
You already have sample PDFs in the `input/` directory. Try processing them:

```bash
# 1. Start the app
./scripts/launch.sh

# 2. Open browser to http://localhost:7860
# 3. Select output formats (Markdown, HTML, JSON)
# 4. Click "Batch Processing" tab
# 5. Click "Process Batch"
# 6. Check output/ folder for results!
```

### Example 2: Extract Figures from PDFs
```bash
# 1. Configure settings:
#    - Output: Markdown, JSON
#    - ✅ Extract Figures
# 2. Upload or batch process PDFs
# 3. Get:
#    - Document text in Markdown/JSON
#    - Figures in output/figures/[document_name]/
```

### Example 3: OCR Scanned Documents
```bash
# 1. Configure settings:
#    - OCR Engine: EasyOCR
#    - ✅ Force Full Page OCR
# 2. Upload scanned PDF
# 3. Get text extracted via OCR
```

### Example 4: Convert CSV to Multiple Formats
```bash
# 1. Select: Markdown, HTML, JSON
# 2. Upload CSV file
# 3. Get formatted tables in all formats
```

### Example 5: Multimodal Export
```bash
# 1. Select: Markdown
# 2. ✅ Multimodal Export
# 3. Upload document with images
# 4. Get self-contained Markdown with embedded images
```

## 🛑 Stop the Application

```bash
./scripts/stop.sh
```

## 📊 Check Status

```bash
./scripts/status.sh
```

## 🔧 Troubleshooting

### Dependencies not installed?
```bash
./scripts/setup.sh
```

### Port already in use?
```bash
./scripts/launch.sh --port 8080
```

### Application won't stop?
```bash
./scripts/stop.sh --force
```

### Check if everything is working?
```bash
./scripts/test.sh
```

## 📚 Need More Help?

- **Full Documentation**: [docs/README.md](docs/README.md)
- **Workflow Diagrams**: [docs/workflows.md](docs/workflows.md)
- **Main README**: [README.md](README.md)

## 💡 Pro Tips

1. **GPU Acceleration**: Use `--gpu` flag for 3-5x faster processing with CUDA GPUs
2. **Background Mode**: Use `--detached` to run the app in the background
3. **OCR Selection**:
   - EasyOCR: Best for multilingual documents
   - Tesseract: Traditional OCR, requires installation
   - macOS Vision: Native macOS OCR
4. **Figure Extraction**: Great for extracting diagrams, charts, and images
5. **Multimodal Export**: Creates self-contained Markdown files with embedded images
6. **Force OCR**: Use for scanned documents or poor quality PDFs
7. **CSV Processing**: Automatically converts to formatted tables
8. **XBRL Support**: Extract financial data from XBRL documents
9. **Output Management**: Use the "Output Management" tab to clean old files
10. **Batch Processing**: Process multiple documents with consistent settings
11. **Format Selection**: Choose only needed formats to save processing time
12. **Progress Tracking**: Monitor real-time progress including figure extraction

---

**That's it!** You're ready to parse documents with Docling! 🎉