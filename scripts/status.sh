#!/bin/bash

###############################################################################
# Docling Parser Application Status Checker
# 
# This script checks the status of the Docling document parser application.
#
# Usage:
#   ./scripts/status.sh
###############################################################################

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

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║      Docling Document Parser - Status Check               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if PID file exists
if [ ! -f "$PID_FILE" ]; then
    print_warning "Application Status: NOT RUNNING"
    echo ""
    print_info "No PID file found at: $PID_FILE"
    print_info "To start the application, run: ./scripts/launch.sh"
    echo ""
    exit 0
fi

# Read PID
APP_PID=$(cat "$PID_FILE")

# Check if process is running
if ps -p "$APP_PID" > /dev/null 2>&1; then
    print_success "Application Status: RUNNING"
    echo ""
    echo "Process Information:"
    echo "  - PID: $APP_PID"
    echo "  - Command: $(ps -p $APP_PID -o comm=)"
    echo "  - Started: $(ps -p $APP_PID -o lstart=)"
    echo "  - CPU: $(ps -p $APP_PID -o %cpu=)%"
    echo "  - Memory: $(ps -p $APP_PID -o %mem=)%"
    echo ""
    
    # Try to detect port
    if command -v lsof &> /dev/null; then
        PORT=$(lsof -Pan -p $APP_PID -i | grep LISTEN | awk '{print $9}' | cut -d: -f2 | head -1)
        if [ ! -z "$PORT" ]; then
            echo "Network Information:"
            echo "  - Port: $PORT"
            echo "  - URL: http://localhost:$PORT"
            echo ""
        fi
    fi
    
    # Check log file
    if [ -f "$LOG_FILE" ]; then
        echo "Log File:"
        echo "  - Location: $LOG_FILE"
        echo "  - Size: $(du -h "$LOG_FILE" | cut -f1)"
        echo "  - Last Modified: $(date -r "$LOG_FILE" '+%Y-%m-%d %H:%M:%S')"
        echo ""
        print_info "Last 5 log entries:"
        tail -n 5 "$LOG_FILE" | sed 's/^/  /'
    fi
    
    echo ""
    print_info "To stop the application, run: ./scripts/stop.sh"
    print_info "To view live logs, run: tail -f $LOG_FILE"
else
    print_error "Application Status: STOPPED (stale PID file)"
    echo ""
    print_warning "PID file exists but process is not running"
    print_info "Cleaning up stale PID file..."
    rm -f "$PID_FILE"
    print_success "Cleaned up"
    echo ""
    print_info "To start the application, run: ./scripts/launch.sh"
fi

echo ""

# Made with Bob
