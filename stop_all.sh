#!/bin/bash

echo "🛑 Stopping TrouveUnCadeau Services..."
echo "======================================"

pkill -f "uvicorn backend.app.main:app"
pkill -f "streamlit run frontend/app.py"

sleep 2

echo "✅ All services stopped"
