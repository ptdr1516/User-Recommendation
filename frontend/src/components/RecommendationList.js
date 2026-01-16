import React from 'react';
import './RecommendationList.css';

function RecommendationList({ recommendations }) {
  const getDifficultyColor = (difficulty) => {
    const colors = {
      'Beginner': '#4caf50',
      'Intermediate': '#ff9800',
      'Advanced': '#f44336',
      'Mixed': '#9c27b0'
    };
    return colors[difficulty] || '#666';
  };

  const formatSimilarityScore = (score) => {
    return (score * 100).toFixed(1);
  };

  return (
    <div className="recommendation-list">
      <h2>Recommended Courses ({recommendations.length})</h2>
      
      <div className="recommendations-grid">
        {recommendations.map((rec, index) => (
          <div key={index} className="recommendation-card">
            <div className="card-header">
              <h3>{rec.course_title}</h3>
              <div className="similarity-badge">
                {formatSimilarityScore(rec.similarity_score)}% match
              </div>
            </div>
            
            <div className="card-body">
              <div className="course-info">
                <div className="info-item">
                  <span className="info-label">Organization:</span>
                  <span className="info-value">{rec.organization}</span>
                </div>
                
                <div className="info-item">
                  <span className="info-label">Certificate:</span>
                  <span className="info-value">{rec.certificate_type}</span>
                </div>
                
                <div className="info-item">
                  <span className="info-label">Difficulty:</span>
                  <span 
                    className="info-value difficulty-badge"
                    style={{ color: getDifficultyColor(rec.difficulty) }}
                  >
                    {rec.difficulty}
                  </span>
                </div>
                
                <div className="info-item">
                  <span className="info-label">Rating:</span>
                  <span className="info-value rating">
                    {'⭐'.repeat(Math.floor(rec.rating))}
                    {rec.rating.toFixed(1)}
                  </span>
                </div>
                
                <div className="info-item">
                  <span className="info-label">Enrollments:</span>
                  <span className="info-value">{rec.students_enrolled}</span>
                </div>
              </div>
              
              <div className="explanation">
                <strong>Why recommended:</strong> {rec.explanation}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RecommendationList;
