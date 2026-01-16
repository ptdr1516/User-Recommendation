# 🚀 How to Run - Simple Guide

## ⚡ Quick Commands (Copy & Paste)

### Terminal 1: ML Service

```bash
cd ml-service
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
python train.py
python app.py
```

**✅ Leave this running!** Port: 8000

---

### Terminal 2: Backend

```bash
cd backend
npm install
npm start
```

**✅ Leave this running!** Port: 3001

---

### Terminal 3: Frontend

```bash
cd frontend
npm install
echo REACT_APP_API_URL=http://localhost:3001 > .env    # Windows
# echo "REACT_APP_API_URL=http://localhost:3001" > .env  # Mac/Linux
npm start
```

**✅ Browser opens automatically!** Port: 3000

---

## 📋 Detailed Steps

For complete instructions, see: **`STEP_BY_STEP_GUIDE.md`**

---

## ✅ Check Everything is Running

| Service | URL | Check |
|---------|-----|-------|
| ML Service | http://localhost:8000/health | ✅ |
| Backend | http://localhost:3001/health | ✅ |
| Frontend | http://localhost:3000 | ✅ |

---

## 🎯 Use the App

1. Open: http://localhost:3000
2. Fill form (difficulty, courses, etc.)
3. Click "Get Recommendations"
4. See results!

---

## 🛑 To Stop

Press `Ctrl+C` in each terminal (in reverse order: Frontend → Backend → ML Service)
