#!/bin/bash
# run_local.sh - Launches the FairLens platform in local demo mode

echo "🚀 Starting FairLens in Local Mode (No GCP required)..."

# Ensure database is seeded
echo "📦 Checking local database..."
python3 scripts/seed_local_db.py

# Start the FastAPI backend in the background
echo "⚡ Starting backend (FastAPI)..."
export LOCAL_MODE=true
export DEV_MODE=true
cd console/backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ../..

# Wait for backend to start
sleep 2

# Start the Vite frontend
echo "🎨 Starting frontend (Vite)..."
cd console/frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ FairLens is running!"
echo "👉 Backend API: http://localhost:8000"
echo "👉 Frontend UI: http://localhost:5173"
echo "Press Ctrl+C to stop both servers."

# Trap Ctrl+C to kill both background processes
trap "echo '\n🛑 Stopping FairLens...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM

# Keep script running
wait
