# 🚀 Quick Start Guide

Get started with **Docling Factory** in 3 simple steps!

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
- Install all required dependencies
- Set up project directories

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

### Option A: Individual Upload

1. Open http://localhost:7860 in your browser
2. **Select output formats** using checkboxes:
   - ✅ **Markdown** - Human-readable text format
   - ✅ **HTML** - Web-ready format
   - ✅ **JSON** - Structured data format
3. Go to the **"📤 Individual Upload"** tab
4. Click **"Upload Document"**
5. Select your file (PDF, DOCX, PPTX, etc.)
6. Click **"🚀 Parse Document"**
7. **Watch real-time progress** as your document is processed
8. View results in separate tabs for each format!

### Option B: Batch Processing

1. Copy your documents to the `input/` folder
2. Open http://localhost:7860 in your browser
3. **Select output formats** using checkboxes (Markdown, HTML, JSON)
4. Go to the **"📦 Batch Processing"** tab
5. Click **"🚀 Process Batch"**
6. **Monitor progress** with the progress bar showing "Processing file X/Y..."
7. All documents are processed automatically!

Results are saved in the `output/` folder with timestamps in your selected formats.

## 📊 Example

You already have sample PDFs in the `input/` directory:
- `Denaire.pdf`
- `SArl Pole Position.pdf`

Try batch processing them with multiple formats:

```bash
# 1. Start the app
./scripts/launch.sh

# 2. Open browser to http://localhost:7860
# 3. Select all output formats (Markdown, HTML, JSON)
# 4. Click "Batch Processing" tab
# 5. Click "Process Batch"
# 6. Watch the progress bar update
# 7. Check output/ folder for results in all formats!
```

You'll get 6 output files (3 formats × 2 documents):
- `Denaire_YYYYMMDD_HHMMSS.md`
- `Denaire_YYYYMMDD_HHMMSS.html`
- `Denaire_YYYYMMDD_HHMMSS.json`
- `SArl_Pole_Position_YYYYMMDD_HHMMSS.md`
- `SArl_Pole_Position_YYYYMMDD_HHMMSS.html`
- `SArl_Pole_Position_YYYYMMDD_HHMMSS.json`

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

1. **GPU Acceleration**: If you have a CUDA GPU, use `--gpu` flag for 3-5x faster processing
2. **Background Mode**: Use `--detached` to run the app in the background
3. **Multiple Formats**: Select only the formats you need to save processing time
4. **Progress Tracking**: Watch the progress display to monitor document processing
5. **HTML Output**: Perfect for viewing documents in a web browser
6. **Output Management**: Use the "Output Management" tab to clean old files
7. **Logs**: Check `logs/app.log` for detailed processing information
8. **Format Selection**: Your format preferences are remembered across sessions

---

**That's it!** You're ready to parse documents with Docling! 🎉