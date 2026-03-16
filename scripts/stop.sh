#!/bin/bash

###############################################################################
# Docling Parser Application Stopper
# 
# This script stops the running Docling document parser application.
#
# Usage:
#   ./scripts/stop.sh [OPTIONS]
#
# Options:
#   --force, -f    Force kill the application
#   --help, -h     Show this help message
###############################################################################

set -e  # Exit on error

# Default values
FORCE=false
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PID_FILE="$PROJECT_DIR/.docling_app.pid"

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
Docling Parser Application Stopper

Usage: $0 [OPTIONS]

Options:
    --force, -f    Force kill the application (SIGKILL)
    --help, -h     Show this help message

Examples:
    # Gracefully stop the application
    $0

    # Force stop the application
    $0 --force

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--force)
            FORCE=true
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

# Check if PID file exists
if [ ! -f "$PID_FILE" ]; then
    print_warning "No PID file found. Application may not be running."
    
    # Try to find the process anyway
    print_info "Searching for running Gradio processes..."
    PIDS=$(pgrep -f "python.*app.py" || true)
    
    if [ -z "$PIDS" ]; then
        print_info "No running application found."
        exit 0
    else
        print_warning "Found running process(es): $PIDS"
        read -p "Do you want to stop these processes? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Operation cancelled."
            exit 0
        fi
        
        for PID in $PIDS; do
            if [ "$FORCE" = true ]; then
                print_info "Force killing process $PID..."
                kill -9 $PID 2>/dev/null || true
            else
                print_info "Stopping process $PID..."
                kill $PID 2>/dev/null || true
            fi
        done
        
        sleep 2
        print_success "Process(es) stopped."
        exit 0
    fi
fi

# Read PID from file
APP_PID=$(cat "$PID_FILE")

# Check if process is running
if ! ps -p "$APP_PID" > /dev/null 2>&1; then
    print_warning "Application is not running (stale PID: $APP_PID)"
    rm -f "$PID_FILE"
    exit 0
fi

# Display information
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║         Stopping Docling Document Parser                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
print_info "Application PID: $APP_PID"

# Stop the application
if [ "$FORCE" = true ]; then
    print_warning "Force stopping application..."
    kill -9 "$APP_PID" 2>/dev/null || true
else
    print_info "Gracefully stopping application..."
    kill "$APP_PID" 2>/dev/null || true
    
    # Wait for process to stop (max 10 seconds)
    print_info "Waiting for application to stop..."
    for i in {1..10}; do
        if ! ps -p "$APP_PID" > /dev/null 2>&1; then
            break
        fi
        sleep 1
        echo -n "."
    done
    echo ""
    
    # Check if still running
    if ps -p "$APP_PID" > /dev/null 2>&1; then
        print_warning "Application did not stop gracefully. Force stopping..."
        kill -9 "$APP_PID" 2>/dev/null || true
        sleep 1
    fi
fi

# Verify process is stopped
if ps -p "$APP_PID" > /dev/null 2>&1; then
    print_error "Failed to stop application (PID: $APP_PID)"
    exit 1
else
    print_success "Application stopped successfully!"
    rm -f "$PID_FILE"
fi

# Clean up any orphaned processes
print_info "Checking for orphaned processes..."
ORPHANS=$(pgrep -f "python.*app.py" || true)
if [ ! -z "$ORPHANS" ]; then
    print_warning "Found orphaned processes: $ORPHANS"
    for PID in $ORPHANS; do
        kill -9 $PID 2>/dev/null || true
    done
    print_success "Orphaned processes cleaned up."
fi

echo ""
print_info "Application has been stopped."
print_info "To start again, run: ./scripts/launch.sh"
echo ""

# Made with Bob
