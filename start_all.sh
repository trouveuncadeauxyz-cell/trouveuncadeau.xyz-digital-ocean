#!/bin/bash

echo "🚀 Starting TrouveUnCadeau Services..."
echo "======================================"

cd /var/www/trouveuncadeau/trouveuncadeau

# Activate virtual environment
source venv/bin/activate

# Kill any existing processes
echo "🧹 Cleaning up old processes..."
pkill -f "uvicorn backend.app.main:app" 2>/dev/null
pkill -f "streamlit run frontend/app.py" 2>/dev/null
sleep 2

# Start Backend API
echo "🔧 Starting Backend API on port 8000..."
nohup uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload > backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Wait for backend to be ready
echo "⏳ Waiting for backend to start..."
sleep 5

# Start Frontend
echo "🎨 Starting Frontend on port 8501..."
nohup streamlit run frontend/app.py --server.port 8502 --server.address 0.0.0.0 > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

# Wait a moment
sleep 3

echo ""
echo "✅ Services started successfully!"
echo "======================================"
echo "📍 Backend API:  http://localhost:8000"
echo "📍 API Docs:     http://localhost:8000/api/docs"
echo "📍 Frontend:     http://localhost:8501"
echo ""
echo "📋 View logs:"
echo "   Backend:  tail -f backend.log"
echo "   Frontend: tail -f frontend.log"
echo ""
echo "🛑 Stop services:"
echo "   ./stop_all.sh"
