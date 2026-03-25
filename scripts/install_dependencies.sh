#!/bin/bash
# Installation script for Docling Factory with proper dependency ordering
# This script ensures Python 3.12 compatibility by installing dependencies in the correct order

set -e  # Exit on error

echo "🚀 Installing Docling Factory Dependencies"
echo "=========================================="
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "📌 Python version: $PYTHON_VERSION"

if [[ "$PYTHON_VERSION" != "3.12" ]]; then
    echo "⚠️  Warning: This script is optimized for Python 3.12"
    echo "   Your version: $PYTHON_VERSION"
    echo ""
fi

# Step 1: Create/activate virtual environment
echo "📦 Step 1: Setting up virtual environment..."
if [ ! -d "venv" ]; then
    echo "Creating new virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Step 2: Upgrade pip (constrain setuptools for compatibility)
echo "📦 Step 2: Upgrading pip..."
pip install --upgrade pip "setuptools<80" wheel
echo "✅ pip upgraded (setuptools<80 for vllm/PyTorch compatibility)"
echo ""

# Step 3: Install numpy first (critical for Python 3.12)
echo "📦 Step 3: Installing numpy (Python 3.12 compatible version)..."
pip install "numpy>=1.24.0,<2.0.0"
echo "✅ numpy installed"
echo ""

# Step 4: Install opencv-python-headless (uses pre-built wheel with numpy already installed)
echo "📦 Step 4: Installing opencv-python-headless..."
pip install "opencv-python-headless>=4.8.0,<5.0.0"
echo "✅ opencv-python-headless installed"
echo ""

# Step 5: Install PyTorch and torchvision
echo "📦 Step 5: Installing PyTorch and torchvision..."
pip install "torch>=2.0.0" "torchvision>=0.15.0"
echo "✅ PyTorch installed"
echo ""

# Step 6: Install remaining dependencies from requirements.txt
echo "📦 Step 6: Installing remaining dependencies..."
pip install -r requirements.txt
echo "✅ All dependencies installed"
echo ""

# Verify critical packages
echo "🔍 Verifying installation..."
echo ""

# Check Docling
if python -c "import docling" 2>/dev/null; then
    echo "✅ Docling: Installed"
else
    echo "❌ Docling: Not installed"
fi

# Check EasyOCR
if python -c "import easyocr" 2>/dev/null; then
    EASYOCR_VERSION=$(python -c "import easyocr; print(easyocr.__version__)")
    echo "✅ EasyOCR: $EASYOCR_VERSION"
else
    echo "❌ EasyOCR: Not installed"
fi

# Check OpenCV
if python -c "import cv2" 2>/dev/null; then
    OPENCV_VERSION=$(python -c "import cv2; print(cv2.__version__)")
    echo "✅ OpenCV: $OPENCV_VERSION"
else
    echo "❌ OpenCV: Not installed"
fi

# Check Gradio
if python -c "import gradio" 2>/dev/null; then
    GRADIO_VERSION=$(python -c "import gradio; print(gradio.__version__)")
    echo "✅ Gradio: $GRADIO_VERSION"
else
    echo "❌ Gradio: Not installed"
fi

# Check OpenSearch
if python -c "import opensearchpy" 2>/dev/null; then
    echo "✅ OpenSearch Python client: Installed"
else
    echo "❌ OpenSearch Python client: Not installed"
fi

# Check Ollama
if python -c "import ollama" 2>/dev/null; then
    echo "✅ Ollama: Installed"
else
    echo "❌ Ollama: Not installed"
fi

echo ""
echo "=========================================="
echo "✅ Installation complete in virtual environment!"
echo ""
echo "⚠️  IMPORTANT: Always activate the virtual environment before running the app:"
echo "   source venv/bin/activate"
echo ""
echo "Next steps:"
echo "1. Activate venv: source venv/bin/activate"
echo "2. Start OpenSearch: docker-compose -f docker-compose-opensearch.yml up -d"
echo "3. Start Ollama: ollama serve"
echo "4. Pull Ollama models: ollama pull llama3.2 && ollama pull nomic-embed-text"
echo "5. Run the app: python app_enhanced.py"
echo ""

# Made with Bob
