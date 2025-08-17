#!/bin/bash

# Start development server with auto-regeneration and live reload
# Usage: ./serve.sh [input.md]

# Auto-detect Python environment
if [ -f "venv/bin/activate" ]; then
    PYTHON="venv/bin/python3"
elif [ -f ".venv/bin/activate" ]; then
    PYTHON=".venv/bin/python3"
else
    PYTHON="python3"
fi

# Default to poster.md if no argument provided
INPUT_FILE="${1:-poster.md}"

if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ Error: $INPUT_FILE not found"
    exit 1
fi

echo "🚀 Starting poster development server..."
echo "📝 Watching: $INPUT_FILE"
echo "🌐 Server: http://localhost:3000"
echo "✨ Auto-regeneration + live reload enabled"
echo ""
echo "💡 Edit and save your markdown file to see changes instantly"
echo "⏹️  Press Ctrl+C to stop everything"
echo ""

# Generate initial version
echo "🔄 Initial generation..."
$PYTHON scripts/md_to_poster.py "$INPUT_FILE"
if [ $? -ne 0 ]; then
    echo "❌ Initial generation failed"
    exit 1
fi
echo "✅ Generated output/poster.html"
echo ""

# Function to handle cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping development server..."
    kill $BROWSER_SYNC_PID 2>/dev/null
    kill $WATCHER_PID 2>/dev/null
    exit 0
}

# Set up signal handling
trap cleanup SIGINT SIGTERM

# Start file watcher in background
if command -v inotifywait &> /dev/null; then
    {
        while inotifywait -e modify "$INPUT_FILE" 2>/dev/null; do
            echo "📝 Change detected in $INPUT_FILE"
            echo "🔄 Regenerating..."
            
            $PYTHON scripts/md_to_poster.py "$INPUT_FILE"
            
            if [ $? -eq 0 ]; then
                echo "✅ Updated ($(date '+%H:%M:%S'))"
            else
                echo "❌ Generation failed"
            fi
        done
    } &
    WATCHER_PID=$!
    echo "👀 File watcher started"
else
    echo "⚠️  Warning: inotifywait not found (install with: sudo apt-get install inotify-tools)"
    echo "📝 Auto-regeneration disabled - you'll need to run ./generate_poster.sh manually"
fi

echo "🌐 Starting browser-sync server..."
echo ""

# Start browser-sync server
npx browser-sync start --server --files "output/*.html" --no-notify --port 3000 --startPath "output/poster.html" &
BROWSER_SYNC_PID=$!

# Wait for browser-sync to finish
wait $BROWSER_SYNC_PID