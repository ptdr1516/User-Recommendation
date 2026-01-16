# 🎯 START HERE - How to Run

## 📌 Prerequisites

Check you have these installed:
- ✅ Python 3.8+ (`python --version`)
- ✅ Node.js 16+ (`node --version`)
- ✅ npm (`npm --version`)

---

## 🚀 Running the System (3 Steps)

### Step 1️⃣: Train & Start ML Service

**Open Terminal 1:**

```bash
cd ml-service
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
python train.py                # Train model (one-time)
python app.py                  # Start service
```

**✅ Wait for:** `Uvicorn running on http://0.0.0.0:8000`

**Keep this terminal open!**

---

### Step 2️⃣: Start Backend

**Open Terminal 2 (NEW terminal):**

```bash
cd backend
npm install
npm start
```

**✅ Wait for:** `Backend server running on port 3001`

**Keep this terminal open!**

---

### Step 3️⃣: Start Frontend

**Open Terminal 3 (NEW terminal):**

```bash
cd frontend
npm install
echo REACT_APP_API_URL=http://localhost:3001 > .env    # Windows
# echo "REACT_APP_API_URL=http://localhost:3001" > .env  # Mac/Linux
npm start
```

**✅ Browser opens automatically at:** `http://localhost:3000`

---

## ✅ You're Done!

Now you have:
- ✅ ML Service running (port 8000)
- ✅ Backend running (port 3001)  
- ✅ Frontend running (port 3000)

**Use the app:** Fill the form and click "Get Recommendations"!

---

## 📚 Need More Details?

- **Detailed steps:** See [STEP_BY_STEP_GUIDE.md](STEP_BY_STEP_GUIDE.md)
- **Quick commands:** See [RUN.md](RUN.md)
- **Full documentation:** See [README.md](README.md)

---

## ❌ Troubleshooting

| Problem | Solution |
|---------|----------|
| "Model not trained" | Run `python train.py` first |
| "Connection refused" | Check all services are running |
| Port in use | Kill process or change port in `.env` |
| Module errors | Run `npm install` or `pip install -r requirements.txt` |

---

**🎓 Happy recommending!**
