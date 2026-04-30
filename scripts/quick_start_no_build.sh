#!/bin/bash

# Quick Start Script - No Docker Build Required
# This script starts only the pre-built services and runs the app locally

set -e

echo "🚀 Docling Factory - Quick Start (No Build)"
echo "==========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker Desktop.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker is running${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.11+${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python is installed${NC}"

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✓ Python version: $PYTHON_VERSION${NC}"

# Step 1: Start pre-built Docker services only
echo ""
echo "📦 Step 1: Starting pre-built Docker services..."
echo "   - OpenSearch (vector database)"
echo "   - LiteLLM (AI Gateway)"
echo "   - PostgreSQL (LiteLLM database)"
echo ""

docker-compose up -d opensearch litellm-db litellm

# Wait for services to be ready
echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check OpenSearch
echo -n "   Checking OpenSearch... "
if curl -s http://localhost:9200 > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${YELLOW}⚠ Not ready yet (this is normal)${NC}"
fi

# Check LiteLLM
echo -n "   Checking LiteLLM... "
if curl -s http://localhost:4000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${YELLOW}⚠ Not ready yet (this is normal)${NC}"
fi

# Step 2: Check if Python dependencies are installed
echo ""
echo "📚 Step 2: Checking Python dependencies..."

if python3 -c "import gradio" 2>/dev/null; then
    echo -e "${GREEN}✓ Dependencies already installed${NC}"
else
    echo -e "${YELLOW}⚠ Dependencies not found. Installing...${NC}"
    echo ""
    echo "This may take 10-20 minutes for the first time."
    echo "Heavy packages: PyTorch, EasyOCR, Docling"
    echo ""
    
    # Ask user if they want to install
    read -p "Install Python dependencies now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip3 install -r requirements.txt
        echo -e "${GREEN}✓ Dependencies installed${NC}"
    else
        echo -e "${RED}❌ Cannot continue without dependencies${NC}"
        exit 1
    fi
fi

# Step 3: Set environment variables
echo ""
echo "🔧 Step 3: Setting environment variables..."

export OPENSEARCH_HOST=localhost
export OPENSEARCH_PORT=9200
export LITELLM_API_BASE=http://localhost:4000
export LITELLM_API_KEY=sk-1234
export OLLAMA_BASE_URL=http://localhost:11434
export GRADIO_SERVER_NAME=0.0.0.0
export GRADIO_SERVER_PORT=7860

echo -e "${GREEN}✓ Environment configured${NC}"

# Step 4: Check if Ollama is running (optional)
echo ""
echo "🤖 Step 4: Checking Ollama (optional)..."

if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Ollama is running${NC}"
    echo "   You can use local Ollama models"
else
    echo -e "${YELLOW}⚠ Ollama is not running${NC}"
    echo "   You can still use LiteLLM with remote models"
    echo "   To use Ollama: brew install ollama && ollama serve"
fi

# Step 5: Start the application
echo ""
echo "🎯 Step 5: Starting Docling Factory..."
echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}Application will start at:${NC}"
echo -e "${GREEN}http://localhost:7860${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Run the application
python3 app_enhanced.py

# Cleanup on exit
trap 'echo ""; echo "🛑 Stopping services..."; docker-compose down; echo "✓ Services stopped"' EXIT

# Made with Bob
