#!/bin/bash

###############################################################################
# Docling Parser Application Launcher
# 
# This script launches the Docling document parser application with various
# options including detached mode, custom port, and GPU support.
#
# Usage:
#   ./scripts/launch.sh [OPTIONS]
#
# Options:
#   --detached, -d     Run in detached mode (background)
#   --port PORT, -p    Specify custom port (default: 7860)
#   --gpu, -g          Enable GPU acceleration
#   --share, -s        Create public share link
#   --help, -h         Show this help message
###############################################################################

set -e  # Exit on error

# Default values
DETACHED=false
PORT=7860
GPU=false
SHARE=false
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PID_FILE="$PROJECT_DIR/.docling_app.pid"
LOG_FILE="$PROJECT_DIR/logs/app.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
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

# Function to show help
show_help() {
    cat << EOF
Docling Parser Application Launcher

Usage: $0 [OPTIONS]

Options:
    --detached, -d     Run in detached mode (background)
    --port PORT, -p    Specify custom port (default: 7860)
    --gpu, -g          Enable GPU acceleration
    --share, -s        Create public share link
    --help, -h         Show this help message

Examples:
    # Start in foreground
    $0

    # Start in background on port 8080
    $0 --detached --port 8080

    # Start with GPU acceleration
    $0 --gpu

    # Start with public sharing
    $0 --share --detached

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--detached)
            DETACHED=true
            shift
            ;;
        -p|--port)
            PORT="$2"
            shift 2
            ;;
        -g|--gpu)
            GPU=true
            shift
            ;;
        -s|--share)
            SHARE=true
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

# Check if application is already running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        print_warning "Application is already running (PID: $OLD_PID)"
        print_info "Use './scripts/stop.sh' to stop it first"
        exit 1
    else
        print_warning "Stale PID file found. Removing..."
        rm -f "$PID_FILE"
    fi
fi

# Change to project directory
cd "$PROJECT_DIR"

# Create necessary directories
print_info "Creating necessary directories..."
mkdir -p input output logs

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_warning "Virtual environment not found. Creating one..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if ! python -c "import gradio" 2>/dev/null; then
    print_warning "Dependencies not installed. Installing..."
    if [ "$GPU" = true ]; then
        pip install -r requirements-gpu.txt
    else
        pip install -r requirements.txt
    fi
    print_success "Dependencies installed"
fi

# Set environment variables
export DOCLING_PORT=$PORT
export DOCLING_USE_GPU=$GPU
export DOCLING_SHARE=$SHARE

# Build the Python command
PYTHON_CMD="python app.py"

# Display startup information
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║         Docling Document Parser Application               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
print_info "Configuration:"
echo "  - Port: $PORT"
echo "  - GPU: $GPU"
echo "  - Share: $SHARE"
echo "  - Mode: $([ "$DETACHED" = true ] && echo "Detached (Background)" || echo "Foreground")"
echo ""

# Launch the application
if [ "$DETACHED" = true ]; then
    print_info "Starting application in detached mode..."
    
    # Start the application in background
    nohup $PYTHON_CMD > "$LOG_FILE" 2>&1 &
    APP_PID=$!
    
    # Save PID to file
    echo $APP_PID > "$PID_FILE"
    
    # Wait a moment to check if it started successfully
    sleep 3
    
    if ps -p $APP_PID > /dev/null 2>&1; then
        print_success "Application started successfully!"
        echo ""
        print_info "Application Details:"
        echo "  - PID: $APP_PID"
        echo "  - URL: http://localhost:$PORT"
        echo "  - Log file: $LOG_FILE"
        echo ""
        print_info "To stop the application, run: ./scripts/stop.sh"
        print_info "To view logs, run: tail -f $LOG_FILE"
    else
        print_error "Application failed to start. Check logs: $LOG_FILE"
        rm -f "$PID_FILE"
        exit 1
    fi
else
    print_info "Starting application in foreground mode..."
    print_info "Press Ctrl+C to stop the application"
    echo ""
    
    # Trap Ctrl+C to clean up
    trap 'print_info "Shutting down..."; rm -f "$PID_FILE"; exit 0' INT TERM
    
    # Save PID
    echo $$ > "$PID_FILE"
    
    # Start the application
    $PYTHON_CMD
    
    # Clean up PID file on exit
    rm -f "$PID_FILE"
fi

# Made with Bob
