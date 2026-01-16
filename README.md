# 🎓 AI-Powered Smart Course Recommendation Engine

A production-ready course recommendation system using **clustering + similarity scoring** with a **MERN + Python** stack.

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   React     │─────▶│  Node.js     │─────▶│   Python    │
│  Frontend   │      │   Backend    │      │  ML Service │
└─────────────┘      └──────────────┘      └─────────────┘
```

- **Frontend**: React application for user interaction
- **Backend**: Node.js/Express API middleware
- **ML Service**: Python FastAPI service with KMeans clustering and cosine similarity

## 🚀 Quick Start

> **📖 For detailed step-by-step instructions, see [STEP_BY_STEP_GUIDE.md](STEP_BY_STEP_GUIDE.md)**  
> **⚡ For quick commands, see [RUN.md](RUN.md)**

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### 1. Setup ML Service (Python)

```bash
cd ml-service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Train the model
python train.py

# Start ML service
python app.py
```

The ML service will run on `http://localhost:8000`

### 2. Setup Backend (Node.js)

```bash
cd backend
npm install

# Copy environment file
cp .env.example .env

# Start server
npm start
```

The backend will run on `http://localhost:3001`

### 3. Setup Frontend (React)

```bash
cd frontend
npm install

# Create .env file with:
# REACT_APP_API_URL=http://localhost:3001

npm start
```

The frontend will run on `http://localhost:3000`

## 📊 Dataset

The dataset (`data/courses.csv`) contains 890 courses with:
- `course_title`: Course name
- `course_organization`: Offering organization
- `course_Certificate_type`: Certificate type
- `course_rating`: Rating (0-5)
- `course_difficulty`: Beginner/Intermediate/Advanced/Mixed
- `course_students_enrolled`: Enrollment count (e.g., "1.2M")

## 🧠 ML Pipeline

### Feature Engineering

1. **Numeric Normalization**: Ratings and enrollments scaled using StandardScaler
2. **Categorical Encoding**: One-hot encoding for organizations and certificate types
3. **Text Features**: TF-IDF vectorization on course titles
4. **Ordinal Encoding**: Difficulty mapped to numeric scale (Beginner=1, Intermediate=2, Advanced=3, Mixed=2.5)

### Clustering

- **Algorithm**: KMeans
- **K Selection**: Elbow Method (automatic)
- **Output**: Each course assigned to a cluster

### Recommendation Logic

1. **User Profile Creation**: Synthetic profile based on:
   - Preferred difficulty
   - Liked courses (TF-IDF similarity)
   - Preferred organizations
   - Rating bias weight

2. **Similarity Calculation**:
   - Cosine similarity between user profile and all courses
   - **Primary boost**: Same cluster courses (1.2x multiplier)
   - **Secondary boost**: Higher ratings (+0.05 per normalized rating)
   - **Tertiary boost**: Higher enrollments (+0.03 per normalized enrollment)

3. **Ranking**: Sort by final similarity score

## 📡 API Endpoints

### ML Service (FastAPI)

- `GET /health` - Service health check
- `POST /recommend` - Get recommendations
- `GET /courses` - List all courses (paginated)
- `GET /clusters/{cluster_id}` - Get cluster information

### Backend (Express)

- `GET /health` - Health check
- `POST /api/recommend` - Get recommendations (validates and forwards to ML service)
- `GET /api/courses` - List courses
- `GET /api/clusters/:clusterId` - Get cluster info

### Request Example

```json
POST /api/recommend
{
  "preferred_difficulty": "Intermediate",
  "liked_courses": ["Machine Learning", "Python for Everybody"],
  "preferred_organizations": ["Stanford University"],
  "limit": 10,
  "rating_bias": 0.1
}
```

### Response Example

```json
{
  "success": true,
  "recommendations": [
    {
      "course_title": "Deep Learning",
      "organization": "deeplearning.ai",
      "certificate_type": "Specialization",
      "rating": 4.7,
      "difficulty": "Advanced",
      "students_enrolled": "1.8M",
      "similarity_score": 0.91,
      "cluster": 2,
      "explanation": "Same cluster as your preferences; Highly rated course"
    }
  ],
  "count": 10
}
```

## 📈 Evaluation Metrics

After training, the model outputs:

- **Silhouette Score**: Measures cluster quality (-1 to 1, higher is better)
- **Intra-Cluster Similarity**: Average cosine similarity within clusters
- **Optimal K**: Automatically selected via Elbow Method

View metrics in `ml-service/model_metrics.json` and `ml-service/elbow_curve.png`

## 🎯 Key Features

✅ **Production-Ready**: Error handling, input validation, clean architecture  
✅ **Explainable**: Each recommendation includes explanation  
✅ **Scalable**: Modular design, easy to extend  
✅ **Real ML**: Actual clustering and similarity, not hardcoded  
✅ **User Behavior Simulation**: Synthetic profiles from preferences  

## 📁 Project Structure

```
.
├── ml-service/
│   ├── preprocessing.py      # Feature engineering
│   ├── train.py              # Model training
│   ├── recommender.py        # Recommendation engine
│   ├── app.py                # FastAPI service
│   ├── requirements.txt
│   └── *.pkl                 # Trained models (generated)
├── backend/
│   ├── server.js             # Express API
│   ├── package.json
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── data/
│   └── courses.csv           # Dataset
└── README.md
```

## 🔧 Configuration

### Environment Variables

**Backend** (`.env`):
```
PORT=3001
ML_SERVICE_URL=http://localhost:8000
```

**Frontend** (`.env`):
```
REACT_APP_API_URL=http://localhost:3001
```

## 🧪 Testing the System

1. **Train Model**: Run `python ml-service/train.py`
2. **Start Services**: Start ML service, backend, and frontend
3. **Test API**: Use the frontend or curl:

```bash
curl -X POST http://localhost:3001/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "preferred_difficulty": "Intermediate",
    "liked_courses": ["Machine Learning"],
    "limit": 5
  }'
```

## 🎓 Highlights

- **Hybrid Architecture**: Python ML + Node.js API + React UI
- **Real ML Pipeline**: Feature engineering, clustering, similarity scoring
- **Production Patterns**: Error handling, validation, clean separation
- **Explainable AI**: Recommendations include reasoning
- **Scalable Design**: Modular, extensible architecture

## 📝 Notes

- Model artifacts (`.pkl` files) are generated after training
- The dataset is included in `data/courses.csv`
- All services must be running for full functionality
- First run requires training the model (`train.py`)

## 🐛 Troubleshooting

**ML Service won't start**: Ensure model is trained first (`python train.py`)

**Backend can't connect to ML service**: Check `ML_SERVICE_URL` in backend `.env`

**Frontend can't connect to backend**: Check `REACT_APP_API_URL` in frontend `.env`

**No recommendations returned**: Verify dataset is loaded and model is trained

---

Built with ❤️ for production ML systems

