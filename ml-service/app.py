"""
FastAPI Service for ML Inference
Exposes recommendation endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from recommender import CourseRecommender

app = FastAPI(title="Course Recommendation API", version="1.0.0")

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize recommender (lazy loading)
recommender = None

def get_recommender():
    """Lazy load recommender to handle missing files gracefully"""
    global recommender
    if recommender is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, 'kmeans_model.pkl')
        preprocessor_path = os.path.join(script_dir, 'preprocessor.pkl')
        data_path = os.path.join(script_dir, 'courses_with_clusters.csv')
        
        if not all(os.path.exists(p) for p in [model_path, preprocessor_path, data_path]):
            raise HTTPException(
                status_code=503,
                detail="Model not trained. Please run train.py first."
            )
        
        recommender = CourseRecommender(
            model_path=model_path,
            preprocessor_path=preprocessor_path,
            data_path=data_path
        )
    return recommender


class RecommendationRequest(BaseModel):
    """Request model for recommendations"""
    preferred_difficulty: Optional[str] = Field(
        None, 
        description="Preferred difficulty: Beginner, Intermediate, Advanced, or Mixed"
    )
    liked_courses: Optional[List[str]] = Field(
        default_factory=list,
        description="List of course titles user has liked or viewed"
    )
    preferred_organizations: Optional[List[str]] = Field(
        default_factory=list,
        description="List of preferred course organizations"
    )
    limit: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Number of recommendations to return"
    )
    rating_bias: float = Field(
        default=0.1,
        ge=0.0,
        le=1.0,
        description="Weight for rating preference (0-1)"
    )


class RecommendationResponse(BaseModel):
    """Response model for recommendations"""
    course_title: str
    organization: str
    certificate_type: str
    rating: float
    difficulty: str
    students_enrolled: str
    similarity_score: float
    cluster: int
    explanation: str


@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Course Recommendation API",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    """Health check with model status"""
    try:
        rec = get_recommender()
        return {
            "status": "healthy",
            "model_loaded": True,
            "n_courses": len(rec.courses_df)
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "model_loaded": False,
            "error": str(e)
        }


@app.post("/recommend", response_model=List[RecommendationResponse])
def get_recommendations(request: RecommendationRequest):
    """
    Get course recommendations based on user preferences
    
    Validates input and returns personalized recommendations with explanations
    """
    try:
        # Validate difficulty if provided
        if request.preferred_difficulty:
            valid_difficulties = ['Beginner', 'Intermediate', 'Advanced', 'Mixed']
            if request.preferred_difficulty not in valid_difficulties:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid difficulty. Must be one of: {', '.join(valid_difficulties)}"
                )
        
        # Get recommender
        rec = get_recommender()
        
        # Generate recommendations
        recommendations = rec.recommend(
            preferred_difficulty=request.preferred_difficulty,
            liked_courses=request.liked_courses or [],
            preferred_organizations=request.preferred_organizations or [],
            limit=request.limit,
            rating_bias=request.rating_bias
        )
        
        if not recommendations:
            raise HTTPException(
                status_code=404,
                detail="No recommendations found matching your criteria"
            )
        
        return recommendations
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendations: {str(e)}"
        )


@app.get("/clusters/{cluster_id}")
def get_cluster_info(cluster_id: int):
    """Get information about a specific cluster"""
    try:
        rec = get_recommender()
        
        if cluster_id < 0 or cluster_id >= rec.kmeans_model.n_clusters:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid cluster_id. Must be between 0 and {rec.kmeans_model.n_clusters - 1}"
            )
        
        return rec.get_cluster_info(cluster_id)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving cluster info: {str(e)}"
        )


@app.get("/courses")
def list_courses(limit: int = 100, offset: int = 0):
    """List all available courses (paginated)"""
    try:
        rec = get_recommender()
        
        courses = rec.courses_df.iloc[offset:offset+limit]
        
        return {
            "total": len(rec.courses_df),
            "limit": limit,
            "offset": offset,
            "courses": courses.to_dict('records')
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving courses: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
