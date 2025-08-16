#!/bin/bash

# Start browser-sync server with auto-reload for HTML files
echo "Starting poster preview server..."
echo "Your poster will open automatically in the browser"
echo "The page will auto-reload when you save changes to poster.html"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

npx browser-sync start --server --files "*.html" --no-notify --port 3000 --startPath "poster.html"