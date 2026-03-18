#!/bin/bash

echo "🚀 Starting BioBD Enhanced - V4 Interface + V5 Data (1492 Assets)"
echo ""

# Check if port 8765 is in use
if lsof -Pi :8765 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 8765 is already in use. Stopping existing process..."
    lsof -ti :8765 | xargs kill -9 2>/dev/null
    sleep 1
fi

echo "📡 Starting WebSocket server..."
python3 websocket_server.py &
echo $! > .server.pid
echo "✅ Server started"
echo ""
echo "📊 Dashboard: file://$(pwd)/index.html"
echo "WebSocket: ws://localhost:8765"
echo ""
echo "Press Ctrl+C to stop"

wait
