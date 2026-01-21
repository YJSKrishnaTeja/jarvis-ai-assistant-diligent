#!/bin/bash

echo "🚀 Starting Jarvis AI Assistant..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start the backend
echo "🔧 Starting backend server on http://localhost:8000"
cd backend && python app.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Open frontend
echo "🌐 Opening frontend..."
if command -v xdg-open &> /dev/null; then
    xdg-open ../frontend/index.html
elif command -v open &> /dev/null; then
    open ../frontend/index.html
else
    echo "Please open frontend/index.html in your browser"
fi

echo ""
echo "✅ Jarvis is running!"
echo "📡 Backend API: http://localhost:8000"
echo "🌐 Frontend: Open frontend/index.html in your browser"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"

# Wait for user interrupt
wait $BACKEND_PID
