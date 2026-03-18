#!/bin/bash

# BioBD Platform Startup Script
# Starts WebSocket server for real-time asset dashboard

echo "🚀 Starting BioBD Platform..."
echo ""

# Check if port 8765 is in use
if lsof -Pi :8765 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 8765 is already in use. Stopping existing process..."
    lsof -ti :8765 | xargs kill -9 2>/dev/null
    sleep 1
fi

# Start WebSocket server
echo "📡 Starting WebSocket server on port 8765..."
python3 src/websocket_server.py &
SERVER_PID=$!

echo "✅ WebSocket server started (PID: $SERVER_PID)"
echo ""
echo "📊 Dashboard available at:"
echo "   File: frontend/index.html"
echo ""
echo "🔧 To open dashboard:"
echo "   Linux:   xdg-open frontend/index.html"
echo "   macOS:   open frontend/index.html"
echo "   Windows: start frontend/index.html"
echo ""
echo "Press Ctrl+C to stop the server"

# Wait for server
wait $SERVER_PID
