#!/bin/bash

###############################################################################
# Docling Parser Application Test Script
# 
# This script performs basic tests to verify the application setup.
#
# Usage:
#   ./scripts/test.sh
###############################################################################

set -e  # Exit on error

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
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

TEST_PASSED=0
TEST_FAILED=0

run_test() {
    local test_name=$1
    local test_command=$2
    
    echo -n "Testing $test_name... "
    if eval "$test_command" > /dev/null 2>&1; then
        print_success "$test_name"
        ((TEST_PASSED++))
        return 0
    else
        print_error "$test_name"
        ((TEST_FAILED++))
        return 1
    fi
}

cd "$PROJECT_DIR"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║      Docling Document Parser - Test Suite                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Test 1: Check Python version
print_info "Running tests..."
echo ""

run_test "Python 3.8+ installed" "python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)'"

# Test 2: Check if virtual environment exists
run_test "Virtual environment exists" "[ -d venv ]"

# Test 3: Check if requirements files exist
run_test "requirements.txt exists" "[ -f requirements.txt ]"
run_test "requirements-gpu.txt exists" "[ -f requirements-gpu.txt ]"

# Test 4: Check if main files exist
run_test "app.py exists" "[ -f app.py ]"
run_test "docling_parser.py exists" "[ -f docling_parser.py ]"

# Test 5: Check if directories exist
run_test "input/ directory exists" "[ -d input ]"
run_test "output/ directory exists" "[ -d output ]"
run_test "docs/ directory exists" "[ -d docs ]"
run_test "scripts/ directory exists" "[ -d scripts ]"

# Test 6: Check if scripts are executable
run_test "launch.sh is executable" "[ -x scripts/launch.sh ]"
run_test "stop.sh is executable" "[ -x scripts/stop.sh ]"
run_test "status.sh is executable" "[ -x scripts/status.sh ]"
run_test "setup.sh is executable" "[ -x scripts/setup.sh ]"

# Test 7: Check if documentation exists
run_test "README.md exists" "[ -f README.md ]"
run_test "docs/README.md exists" "[ -f docs/README.md ]"
run_test "docs/workflows.md exists" "[ -f docs/workflows.md ]"

# Test 8: Check Python imports (if venv is activated)
if [ -d "venv" ]; then
    source venv/bin/activate 2>/dev/null || true
    
    run_test "Python can import pathlib" "python -c 'import pathlib'"
    run_test "Python can import datetime" "python -c 'import datetime'"
    run_test "Python can import logging" "python -c 'import logging'"
    
    # Optional: Check if dependencies are installed
    if python -c "import gradio" 2>/dev/null; then
        run_test "Gradio is installed" "python -c 'import gradio'"
    else
        print_warning "Gradio not installed (run ./scripts/setup.sh)"
    fi
    
    if python -c "import docling" 2>/dev/null; then
        run_test "Docling is installed" "python -c 'import docling'"
    else
        print_warning "Docling not installed (run ./scripts/setup.sh)"
    fi
fi

# Test 9: Check file syntax
run_test "app.py syntax is valid" "python3 -m py_compile app.py"
run_test "docling_parser.py syntax is valid" "python3 -m py_compile docling_parser.py"

# Test 10: Check if .gitignore exists
run_test ".gitignore exists" "[ -f .gitignore ]"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    Test Results                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Tests Passed: $TEST_PASSED"
echo "Tests Failed: $TEST_FAILED"
echo ""

if [ $TEST_FAILED -eq 0 ]; then
    print_success "All tests passed! ✨"
    echo ""
    print_info "Your application is ready to use!"
    print_info "Start the application with: ./scripts/launch.sh"
    echo ""
    exit 0
else
    print_error "Some tests failed."
    echo ""
    print_info "To fix issues:"
    echo "  1. Run setup: ./scripts/setup.sh"
    echo "  2. Check documentation: docs/README.md"
    echo "  3. Verify all files are present"
    echo ""
    exit 1
fi

# Made with Bob
