# 🚀 Quick Start Guide

## Prerequisites Check

```bash
# Check Python version (need 3.8+)
python --version

# Check Node.js version (need 16+)
node --version

# Check npm
npm --version
```

## Step-by-Step Setup

### Step 1: Train the ML Model

```bash
cd ml-service
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
python train.py
```

**Expected output:**
```
Loading course data...
Loaded 890 courses
Preprocessing features...
Feature matrix shape: (890, X)
Finding optimal number of clusters...
Optimal k: X
Training KMeans with k=X...
Silhouette Score: X.XXXX
Average Intra-Cluster Similarity: X.XXXX
Training complete!
```

### Step 2: Start ML Service

```bash
# Still in ml-service directory with venv activated
python app.py
```

**Expected output:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test it:**
```bash
curl http://localhost:8000/health
```

### Step 3: Start Backend

Open a **new terminal**:

```bash
cd backend
npm install
npm start
```

**Expected output:**
```
🚀 Backend server running on port 3001
📡 ML Service URL: http://localhost:8000
```

**Test it:**
```bash
curl http://localhost:3001/health
```

### Step 4: Start Frontend

Open a **new terminal**:

```bash
cd frontend
npm install

# Create .env file
echo REACT_APP_API_URL=http://localhost:3001 > .env

npm start
```

**Expected output:**
```
Compiled successfully!
You can now view course-recommendation-frontend in the browser.
  Local:            http://localhost:3000
```

## Testing the System

1. Open browser to `http://localhost:3000`
2. Fill in the form:
   - Select difficulty: "Intermediate"
   - Add liked courses: "Machine Learning", "Python for Everybody"
   - Click "Get Recommendations"
3. You should see personalized recommendations with explanations!

## API Testing (Alternative)

```bash
# Get recommendations via API
curl -X POST http://localhost:3001/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "preferred_difficulty": "Intermediate",
    "liked_courses": ["Machine Learning"],
    "limit": 5
  }'
```

## Troubleshooting

### "Model not trained" error
→ Run `python ml-service/train.py` first

### "Connection refused" error
→ Ensure ML service is running on port 8000

### Frontend can't connect
→ Check `REACT_APP_API_URL` in `frontend/.env`

### Port already in use
→ Change ports in `.env` files or kill existing processes

## Next Steps

- Explore different difficulty levels
- Try different course combinations
- Check cluster information: `GET /api/clusters/0`
- View all courses: `GET /api/courses`
