@echo off
REM Setup script for Course Recommendation System (Windows)

echo 🎓 Setting up Course Recommendation System...
echo.

REM Setup ML Service
echo 📦 Setting up ML Service (Python)...
cd ml-service
if not exist "venv" (
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo ✅ ML Service dependencies installed
echo.

REM Train model
echo 🤖 Training ML model...
python train.py
echo ✅ Model trained
deactivate
cd ..

REM Setup Backend
echo 📦 Setting up Backend (Node.js)...
cd backend
call npm install
if not exist ".env" (
    copy .env.example .env
    echo ✅ Created .env file
)
echo ✅ Backend dependencies installed
cd ..

REM Setup Frontend
echo 📦 Setting up Frontend (React)...
cd frontend
call npm install
if not exist ".env" (
    echo REACT_APP_API_URL=http://localhost:3001 > .env
    echo ✅ Created .env file
)
echo ✅ Frontend dependencies installed
cd ..

echo.
echo ✨ Setup complete!
echo.
echo To start the system:
echo   1. ML Service: cd ml-service ^&^& venv\Scripts\activate ^&^& python app.py
echo   2. Backend: cd backend ^&^& npm start
echo   3. Frontend: cd frontend ^&^& npm start
