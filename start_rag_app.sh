#!/bin/bash

# Docling Factory RAG Application Startup Script

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║      Docling Factory RAG - Startup Script                 ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo -e "${YELLOW}Please run: ./scripts/setup.sh${NC}"
    exit 1
fi

# Activate virtual environment
echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
source venv/bin/activate

# Check if OpenSearch is running
echo -e "${BLUE}🔍 Checking OpenSearch...${NC}"
if curl -s http://localhost:9200 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ OpenSearch is running${NC}"
else
    echo -e "${YELLOW}⚠️  OpenSearch is not running${NC}"
    echo -e "${YELLOW}Start it with: podman-compose -f docker-compose-opensearch.yml up -d${NC}"
    echo ""
fi

# Check if Ollama is running
echo -e "${BLUE}🔍 Checking Ollama...${NC}"
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Ollama is running${NC}"
    
    # List available models
    echo -e "${BLUE}📦 Available Ollama models:${NC}"
    ollama list 2>/dev/null | head -10 || echo "  (Could not list models)"
else
    echo -e "${YELLOW}⚠️  Ollama is not running${NC}"
    echo -e "${YELLOW}Make sure Ollama is installed and running${NC}"
    echo ""
fi

echo ""
echo -e "${GREEN}🚀 Starting Docling Factory RAG Application...${NC}"
echo -e "${BLUE}📍 URL: http://localhost:7860${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the application${NC}"
echo ""

# Start the application
python app_enhanced.py

# Made with Bob
