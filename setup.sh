#!/bin/bash
# Setup script for Course Recommendation System

echo "🎓 Setting up Course Recommendation System..."
echo ""

# Setup ML Service
echo "📦 Setting up ML Service (Python)..."
cd ml-service
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
echo "✅ ML Service dependencies installed"
echo ""

# Train model
echo "🤖 Training ML model..."
python train.py
echo "✅ Model trained"
deactivate
cd ..

# Setup Backend
echo "📦 Setting up Backend (Node.js)..."
cd backend
npm install
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Created .env file"
fi
echo "✅ Backend dependencies installed"
cd ..

# Setup Frontend
echo "📦 Setting up Frontend (React)..."
cd frontend
npm install
if [ ! -f ".env" ]; then
    echo "REACT_APP_API_URL=http://localhost:3001" > .env
    echo "✅ Created .env file"
fi
echo "✅ Frontend dependencies installed"
cd ..

echo ""
echo "✨ Setup complete!"
echo ""
echo "To start the system:"
echo "  1. ML Service: cd ml-service && source venv/bin/activate && python app.py"
echo "  2. Backend: cd backend && npm start"
echo "  3. Frontend: cd frontend && npm start"
