#!/bin/bash

echo "🐝 Welcome to MediBee!"
echo ""

# Get API keys from user
read -p "Enter your OPENAI_API_KEY: " OPENAI_KEY
read -p "Enter your GEOAPIFY_API_KEY: " GEOAPIFY_KEY

# Create .env file in backend
echo "OPENAI_API_KEY=$OPENAI_KEY" > backend/.env
echo "GEOAPIFY_API_KEY=$GEOAPIFY_KEY" >> backend/.env

echo ""
echo "✅ API keys saved!"
echo ""

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
pip3 install -r requirements.txt
cd ..

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo ""
echo "🚀 Starting MediBee..."
echo ""

# Start backend
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 &
cd ..

# Start frontend
cd frontend
npm start &
cd ..

echo ""
echo "✅ MediBee is running!"
echo "👉 Open http://localhost:3000 in your browser"
echo ""
echo "Press Ctrl+C to stop."
wait