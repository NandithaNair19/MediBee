@echo off
echo 🐝 Welcome to MediBee!
echo.

set /p OPENAI_KEY="Enter your OPENAI_API_KEY: "
set /p GEOAPIFY_KEY="Enter your GEOAPIFY_API_KEY: "

echo OPENAI_API_KEY=%OPENAI_KEY% > backend\.env
echo GEOAPIFY_API_KEY=%GEOAPIFY_KEY% >> backend\.env

echo.
echo ✅ API keys saved!
echo.

echo 📦 Installing backend dependencies...
cd backend
pip install -r requirements.txt
cd ..

echo 📦 Installing frontend dependencies...
cd frontend
npm install
cd ..

echo.
echo 🚀 Starting MediBee...
echo.

start cmd /k "cd backend && uvicorn main:app --host 0.0.0.0 --port 8000"
start cmd /k "cd frontend && npm start"

echo.
echo ✅ MediBee is running!
echo 👉 Open http://localhost:3000 in your browser