#!/bin/bash

echo "🔄 Starting clean restart of Docling Factory..."
echo ""

# Step 1: Kill any running Python processes for app_enhanced.py
echo "1️⃣ Stopping any running app_enhanced.py processes..."
pkill -f "python.*app_enhanced.py" 2>/dev/null
sleep 2

# Step 2: Clear Python cache
echo "2️⃣ Clearing Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
echo "   ✓ Cache cleared"

# Step 3: Start fresh application
echo "3️⃣ Starting app_enhanced.py..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 IMPORTANT: Open the app in a NEW INCOGNITO/PRIVATE WINDOW"
echo "   Chrome/Edge: Ctrl+Shift+N (Win/Linux) or Cmd+Shift+N (Mac)"
echo "   Firefox: Ctrl+Shift+P (Win/Linux) or Cmd+Shift+P (Mac)"
echo "   Safari: Cmd+Shift+N (Mac)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python3 ./app_enhanced.py

# Made with Bob
