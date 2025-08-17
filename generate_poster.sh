#!/bin/bash

# Complete poster generation pipeline
# Usage: ./generate_poster.sh input.md

# Auto-detect Python environment
if [ -f "venv/bin/activate" ]; then
    # Virtual environment exists, use it
    PYTHON="venv/bin/python3"
elif [ -f ".venv/bin/activate" ]; then
    # Alternative venv naming
    PYTHON=".venv/bin/python3"
else
    # Use system Python
    PYTHON="python3"
fi

if [ $# -eq 0 ]; then
    echo "Usage: ./generate_poster.sh input.md"
    echo "Example: ./generate_poster.sh poster.md"
    exit 1
fi

INPUT_FILE="$1"
BASE_NAME=$(basename "$INPUT_FILE" .md)

echo "🔄 Generating poster from $INPUT_FILE..."

# Step 1: Convert markdown to HTML
echo "📄 Converting markdown to HTML..."
$PYTHON scripts/md_to_poster.py "$INPUT_FILE"

if [ $? -ne 0 ]; then
    echo "❌ Failed to generate HTML"
    exit 1
fi

# Step 2: Convert HTML to PDF
echo "📋 Converting HTML to PDF..."
$PYTHON scripts/html_to_pdf.py output/poster.html "output/${BASE_NAME}.pdf"

if [ $? -ne 0 ]; then
    echo "❌ Failed to generate PDF"
    echo "💡 Install dependencies with:"
    echo "   pip install playwright"
    echo "   playwright install chromium"
    exit 1
fi

echo "✅ Complete! Generated:"
echo "   📄 output/poster.html"
echo "   📋 output/${BASE_NAME}.pdf"
echo ""
echo "🌐 View HTML: ./serve.sh"
echo "📋 Print PDF: output/${BASE_NAME}.pdf (36\" x 24\")"