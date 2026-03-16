#!/bin/bash

###############################################################################
# Docling Parser Application Setup Script
# 
# This script sets up the environment for the Docling document parser.
#
# Usage:
#   ./scripts/setup.sh [OPTIONS]
#
# Options:
#   --gpu, -g      Install GPU-accelerated version
#   --help, -h     Show this help message
###############################################################################

set -e  # Exit on error

# Default values
GPU=false
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

show_help() {
    cat << EOF
Docling Parser Application Setup Script

Usage: $0 [OPTIONS]

Options:
    --gpu, -g      Install GPU-accelerated version (requires CUDA)
    --help, -h     Show this help message

Examples:
    # Setup CPU version
    $0

    # Setup GPU version
    $0 --gpu

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -g|--gpu)
            GPU=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Change to project directory
cd "$PROJECT_DIR"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║      Docling Document Parser - Setup                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
print_info "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_success "Python $PYTHON_VERSION found"

# Check Python version is 3.8+
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    print_error "Python 3.8 or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists"
    read -p "Do you want to recreate it? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Removing existing virtual environment..."
        rm -rf venv
        print_info "Creating new virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    fi
else
    print_info "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
print_success "pip upgraded"

# Install requirements
if [ "$GPU" = true ]; then
    print_info "Installing GPU-accelerated dependencies..."
    print_warning "This may take several minutes..."
    
    # Check if CUDA is available
    if command -v nvcc &> /dev/null; then
        CUDA_VERSION=$(nvcc --version | grep "release" | awk '{print $5}' | cut -d, -f1)
        print_info "CUDA $CUDA_VERSION detected"
    else
        print_warning "CUDA not detected. GPU acceleration may not work."
    fi
    
    pip install -r requirements-gpu.txt
    print_success "GPU dependencies installed"
else
    print_info "Installing CPU dependencies..."
    print_warning "This may take several minutes..."
    pip install -r requirements.txt
    print_success "CPU dependencies installed"
fi

# Create necessary directories
print_info "Creating project directories..."
mkdir -p input output logs
print_success "Directories created"

# Create sample files
print_info "Creating sample configuration files..."

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Application
.docling_app.pid
logs/
output/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.bak
EOF
    print_success ".gitignore created"
fi

# Create README in input directory
if [ ! -f "input/README.md" ]; then
    cat > input/README.md << 'EOF'
# Input Directory

Place your documents here for batch processing.

## Supported Formats

- PDF (`.pdf`)
- Microsoft Word (`.docx`, `.doc`)
- Microsoft PowerPoint (`.pptx`)
- Microsoft Excel (`.xlsx`)
- HTML (`.html`)
- Markdown (`.md`)
- Plain Text (`.txt`)

## Usage

1. Copy your documents to this directory
2. Open the web interface at http://localhost:7860
3. Navigate to the "Batch Processing" tab
4. Click "Process Batch"

All processed documents will be saved in the `output/` directory with timestamps.
EOF
    print_success "input/README.md created"
fi

# Test installation
print_info "Testing installation..."
python -c "import gradio; import docling" 2>/dev/null
if [ $? -eq 0 ]; then
    print_success "Installation test passed"
else
    print_warning "Some imports failed, but this may be normal if dependencies are not fully installed"
fi

# Display summary
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    Setup Complete!                         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
print_success "Environment setup completed successfully!"
echo ""
print_info "Next steps:"
echo "  1. Place documents in the 'input/' directory"
echo "  2. Start the application: ./scripts/launch.sh"
echo "  3. Open your browser: http://localhost:7860"
echo ""
print_info "Useful commands:"
echo "  - Start app: ./scripts/launch.sh"
echo "  - Stop app: ./scripts/stop.sh"
echo "  - Check status: ./scripts/status.sh"
echo "  - Start in background: ./scripts/launch.sh --detached"
if [ "$GPU" = true ]; then
    echo "  - Start with GPU: ./scripts/launch.sh --gpu"
fi
echo ""
print_info "For more information, see: docs/README.md"
echo ""

# Made with Bob
