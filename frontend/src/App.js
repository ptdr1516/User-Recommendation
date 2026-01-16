import React, { useState } from 'react';
import './App.css';
import RecommendationForm from './components/RecommendationForm';
import RecommendationList from './components/RecommendationList';
import LoadingSpinner from './components/LoadingSpinner';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001';

function App() {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleRecommendationRequest = async (formData) => {
    setLoading(true);
    setError(null);
    setRecommendations([]);

    try {
      const response = await fetch(`${API_URL}/api/recommend`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || data.error || 'Failed to get recommendations');
      }

      if (data.success && data.recommendations) {
        setRecommendations(data.recommendations);
      } else {
        throw new Error('Invalid response format');
      }
    } catch (err) {
      setError(err.message || 'An error occurred while fetching recommendations');
      console.error('Recommendation error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎓 AI-Powered Course Recommendation</h1>
        <p>Discover courses tailored to your preferences</p>
      </header>

      <main className="App-main">
        <RecommendationForm onSubmit={handleRecommendationRequest} />
        
        {loading && <LoadingSpinner />}
        
        {error && (
          <div className="error-message">
            <strong>Error:</strong> {error}
          </div>
        )}
        
        {recommendations.length > 0 && (
          <RecommendationList recommendations={recommendations} />
        )}
      </main>
    </div>
  );
}

export default App;
