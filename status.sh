#!/bin/bash

echo "📊 TrouveUnCadeau Service Status"
echo "======================================"

if pgrep -f "uvicorn backend.app.main:app" > /dev/null; then
    echo "✅ Backend:  Running (PID: $(pgrep -f 'uvicorn backend.app.main:app'))"
else
    echo "❌ Backend:  Not running"
fi

if pgrep -f "streamlit run frontend/app.py" > /dev/null; then
    echo "✅ Frontend: Running (PID: $(pgrep -f 'streamlit run frontend/app.py'))"
else
    echo "❌ Frontend: Not running"
fi

echo ""
echo "Recent logs:"
echo "============"
echo "Backend (last 5 lines):"
tail -5 backend.log 2>/dev/null || echo "  No logs yet"
echo ""
echo "Frontend (last 5 lines):"
tail -5 frontend.log 2>/dev/null || echo "  No logs yet"
