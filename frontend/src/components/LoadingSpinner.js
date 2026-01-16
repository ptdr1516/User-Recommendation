import React from 'react';
import './LoadingSpinner.css';

function LoadingSpinner() {
  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <p>Generating personalized recommendations...</p>
    </div>
  );
}

export default LoadingSpinner;
