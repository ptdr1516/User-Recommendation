# 🚀 Step-by-Step Guide to Run the System

## Prerequisites Check

Before starting, ensure you have:

1. **Python 3.8+** installed
   ```bash
   python --version
   ```
   If not installed: Download from [python.org](https://www.python.org/downloads/)

2. **Node.js 16+** installed
   ```bash
   node --version
   ```
   If not installed: Download from [nodejs.org](https://nodejs.org/)

3. **npm** (comes with Node.js)
   ```bash
   npm --version
   ```

---

## Step 1: Train the ML Model

### 1.1 Navigate to ML Service Directory

```bash
cd ml-service
```

### 1.2 Create Virtual Environment

**Windows:**
```bash
python -m venv venv
```

**Mac/Linux:**
```bash
python3 -m venv venv
```

### 1.3 Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 1.4 Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed pandas-2.1.3 numpy-1.24.3 scikit-learn-1.3.2 ...
```

### 1.5 Train the Model

```bash
python train.py
```

**Expected output:**
```
Loading course data...
Loaded 949 courses
Preprocessing features...
Feature matrix shape: (949, X)
Finding optimal number of clusters...
Optimal k: X
Training KMeans with k=X...
Silhouette Score: X.XXXX
Average Intra-Cluster Similarity: X.XXXX
Training complete!
```

**What this does:**
- Loads the course dataset
- Creates feature matrix
- Finds optimal number of clusters
- Trains KMeans model
- Saves model files (`kmeans_model.pkl`, `preprocessor.pkl`)

**Keep this terminal open!** You'll need it for Step 2.

---

## Step 2: Start ML Service (Python FastAPI)

### 2.1 Ensure Virtual Environment is Activated

If you closed the terminal, repeat Step 1.2 and 1.3.

### 2.2 Start the ML Service

```bash
python app.py
```

**Expected output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**✅ ML Service is now running on port 8000**

**Keep this terminal open!** The service must stay running.

### 2.3 Test ML Service (Optional)

Open a **new terminal** and test:

```bash
curl http://localhost:8000/health
```

Or visit in browser: `http://localhost:8000/health`

You should see:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "n_courses": 949
}
```

---

## Step 3: Start Backend (Node.js)

### 3.1 Open a NEW Terminal

**Important:** Keep the ML service terminal running, open a new terminal window.

### 3.2 Navigate to Backend Directory

```bash
cd backend
```

(If you're in a different location, use full path or navigate from project root)

### 3.3 Install Node Dependencies

```bash
npm install
```

**Expected output:**
```
added 50 packages in 5s
```

### 3.4 Create Environment File

**Windows:**
```bash
copy env.example .env
```

**Mac/Linux:**
```bash
cp env.example .env
```

**Or manually create `.env` file with:**
```
PORT=3001
ML_SERVICE_URL=http://localhost:8000
```

### 3.5 Start Backend Server

```bash
npm start
```

**Expected output:**
```
🚀 Backend server running on port 3001
📡 ML Service URL: http://localhost:8000
📍 Health check: http://localhost:3001/health
```

**✅ Backend is now running on port 3001**

**Keep this terminal open!** The backend must stay running.

### 3.6 Test Backend (Optional)

Open a **new terminal** and test:

```bash
curl http://localhost:3001/health
```

You should see:
```json
{
  "status": "healthy",
  "backend": "online",
  "ml_service": {
    "status": "healthy",
    "model_loaded": true
  }
}
```

---

## Step 4: Start Frontend (React)

### 4.1 Open a NEW Terminal

**Important:** Keep ML service and backend terminals running, open a new terminal.

### 4.2 Navigate to Frontend Directory

```bash
cd frontend
```

### 4.3 Install Node Dependencies

```bash
npm install
```

**Expected output:**
```
added 1000+ packages in 30s
```

### 4.4 Create Environment File

**Windows:**
```bash
echo REACT_APP_API_URL=http://localhost:3001 > .env
```

**Mac/Linux:**
```bash
echo "REACT_APP_API_URL=http://localhost:3001" > .env
```

**Or manually create `.env` file in `frontend/` directory with:**
```
REACT_APP_API_URL=http://localhost:3001
```

### 4.5 Start React Development Server

```bash
npm start
```

**Expected output:**
```
Compiled successfully!

You can now view course-recommendation-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000

Note that the development build is not optimized.
```

**✅ Frontend is now running on port 3000**

The browser should automatically open to `http://localhost:3000`

---

## Step 5: Use the Application

### 5.1 Open Browser

Navigate to: `http://localhost:3000`

### 5.2 Fill in the Form

1. **Preferred Difficulty** (optional):
   - Select: "Intermediate"

2. **Liked Courses** (optional):
   - Type: "Machine Learning"
   - Press Enter or click "Add"
   - Type: "Python for Everybody"
   - Press Enter or click "Add"

3. **Preferred Organizations** (optional):
   - Type: "Stanford University"
   - Press Enter or click "Add"

4. **Number of Recommendations**: Leave as 10 (or change)

5. **Rating Preference Weight**: Leave as 0.1 (or adjust)

### 5.3 Get Recommendations

Click **"Get Recommendations"** button

### 5.4 View Results

You should see:
- List of recommended courses
- Similarity scores (match percentage)
- Explanations for each recommendation
- Course details (rating, difficulty, enrollments)

---

## 🎯 Quick Reference: All Services

You should have **3 terminals running**:

| Terminal | Service | Port | Status |
|----------|---------|------|--------|
| Terminal 1 | ML Service (Python) | 8000 | ✅ Running |
| Terminal 2 | Backend (Node.js) | 3001 | ✅ Running |
| Terminal 3 | Frontend (React) | 3000 | ✅ Running |

---

## 🧪 Test via API (Alternative)

If you prefer testing via API instead of the UI:

```bash
curl -X POST http://localhost:3001/api/recommend \
  -H "Content-Type: application/json" \
  -d "{
    \"preferred_difficulty\": \"Intermediate\",
    \"liked_courses\": [\"Machine Learning\"],
    \"limit\": 5
  }"
```

**Windows PowerShell:**
```powershell
Invoke-RestMethod -Uri http://localhost:3001/api/recommend -Method Post -ContentType "application/json" -Body '{"preferred_difficulty":"Intermediate","liked_courses":["Machine Learning"],"limit":5}'
```

---

## 🛑 Stopping the Services

To stop each service, go to its terminal and press:
- **Ctrl + C** (Windows/Linux)
- **Cmd + C** (Mac)

Stop in reverse order:
1. Frontend (Terminal 3)
2. Backend (Terminal 2)
3. ML Service (Terminal 1)

---

## ❌ Troubleshooting

### Error: "Model not trained"
**Solution:** Run `python train.py` in `ml-service/` directory first

### Error: "Connection refused" or "ECONNREFUSED"
**Solution:** 
- Check ML service is running on port 8000
- Check backend is running on port 3001
- Verify `.env` files have correct URLs

### Error: "Port already in use"
**Solution:**
- Find and kill process using the port, OR
- Change port in `.env` files

**Windows - Find process:**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Mac/Linux - Find process:**
```bash
lsof -ti:8000
kill -9 <PID>
```

### Frontend shows "Failed to fetch"
**Solution:**
- Check `REACT_APP_API_URL` in `frontend/.env`
- Ensure backend is running
- Check browser console for errors

### "Module not found" errors
**Solution:**
- Run `npm install` in the directory with the error
- Run `pip install -r requirements.txt` for Python errors

### Virtual environment not activating
**Solution:**
- Windows: Try `venv\Scripts\activate.bat`
- Mac/Linux: Ensure you're using `source venv/bin/activate`

---

## ✅ Success Checklist

- [ ] Python virtual environment created and activated
- [ ] ML model trained (`train.py` completed successfully)
- [ ] ML service running on port 8000
- [ ] Backend running on port 3001
- [ ] Frontend running on port 3000
- [ ] Browser opens to `http://localhost:3000`
- [ ] Can submit form and see recommendations

---

## 🎓 Next Steps

Once everything is running:

1. **Experiment with different preferences**
   - Try different difficulty levels
   - Add/remove liked courses
   - Test various organizations

2. **Explore API endpoints**
   - `GET http://localhost:3001/api/courses`
   - `GET http://localhost:3001/api/clusters/0`

3. **Check model metrics**
   - View `ml-service/model_metrics.json`
   - Check `ml-service/elbow_curve.png`

---

**Need help?** Check the main `README.md` for more details!
