# Input Directory

Place your documents here for batch processing.

## 📋 Supported Formats

- **PDF** (`.pdf`) - Portable Document Format
- **Microsoft Word** (`.docx`, `.doc`) - Word documents
- **Microsoft PowerPoint** (`.pptx`) - Presentations
- **Microsoft Excel** (`.xlsx`) - Spreadsheets
- **HTML** (`.html`) - Web pages
- **Markdown** (`.md`) - Markdown documents
- **Plain Text** (`.txt`) - Text files

## 🚀 Usage

### Batch Processing

1. Copy your documents to this directory
2. Open the web interface at `http://localhost:7860`
3. Navigate to the **"📦 Batch Processing"** tab
4. Click **"🚀 Process Batch"**
5. Check the `output/` directory for results

### Individual Processing

You can also upload files directly through the web interface:
1. Navigate to the **"📤 Individual Upload"** tab
2. Click **"Upload Document"**
3. Select your file
4. Click **"🚀 Parse Document"**

## 📤 Output

All processed documents will be saved in the `output/` directory with:
- Timestamped filenames (e.g., `document_20240316_143052.md`)
- Multiple formats per document (based on your selection):
  - `.md` - Markdown format (human-readable text)
  - `.html` - HTML format (web-ready output)
  - `.json` - JSON format (structured data)

You can select which formats to generate using the checkboxes in the web interface.

## 💡 Tips

- You can process multiple documents at once
- Large files may take longer to process
- Enable GPU acceleration for faster processing (if available)
- The application preserves the original files in this directory

## 🔍 Example

```
input/
├── report.pdf
├── presentation.pptx
└── data.xlsx
```

After batch processing with all formats selected:

```
output/
├── report_20240316_143052.md
├── report_20240316_143052.html
├── report_20240316_143052.json
├── presentation_20240316_143053.md
├── presentation_20240316_143053.html
├── presentation_20240316_143053.json
├── data_20240316_143054.md
├── data_20240316_143054.html
└── data_20240316_143054.json
```

## ⚠️ Notes

- This directory is monitored by the batch processing feature
- Files are not automatically deleted after processing
- You can organize files in subdirectories (batch processing is recursive)
- Maximum file size depends on available system memory