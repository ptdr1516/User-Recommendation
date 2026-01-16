/**
 * Express Server for Course Recommendation API
 * Acts as middleware between frontend and Python ML service
 */

const express = require('express');
const axios = require('axios');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;
const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://localhost:8000';

// Middleware
app.use(cors());
app.use(express.json());

// Request logging middleware
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
});

/**
 * Health check endpoint
 */
app.get('/health', async (req, res) => {
  try {
    const response = await axios.get(`${ML_SERVICE_URL}/health`);
    res.json({
      status: 'healthy',
      backend: 'online',
      ml_service: response.data
    });
  } catch (error) {
    res.status(503).json({
      status: 'unhealthy',
      backend: 'online',
      ml_service: 'offline',
      error: error.message
    });
  }
});

/**
 * Recommendation endpoint
 * Validates input and forwards to ML service
 */
app.post('/api/recommend', async (req, res) => {
  try {
    // Input validation
    const { preferred_difficulty, liked_courses, preferred_organizations, limit, rating_bias } = req.body;

    // Validate difficulty if provided
    if (preferred_difficulty) {
      const validDifficulties = ['Beginner', 'Intermediate', 'Advanced', 'Mixed'];
      if (!validDifficulties.includes(preferred_difficulty)) {
        return res.status(400).json({
          error: 'Invalid difficulty',
          message: `Difficulty must be one of: ${validDifficulties.join(', ')}`
        });
      }
    }

    // Validate limit
    const recommendationLimit = limit && limit > 0 && limit <= 50 ? limit : 10;

    // Validate rating_bias
    const bias = rating_bias !== undefined && rating_bias >= 0 && rating_bias <= 1 
      ? rating_bias 
      : 0.1;

    // Validate arrays
    const courses = Array.isArray(liked_courses) ? liked_courses : [];
    const organizations = Array.isArray(preferred_organizations) ? preferred_organizations : [];

    // Prepare request payload
    const payload = {
      preferred_difficulty: preferred_difficulty || null,
      liked_courses: courses,
      preferred_organizations: organizations,
      limit: recommendationLimit,
      rating_bias: bias
    };

    // Forward to ML service
    const response = await axios.post(`${ML_SERVICE_URL}/recommend`, payload, {
      timeout: 30000 // 30 second timeout
    });

    res.json({
      success: true,
      recommendations: response.data,
      count: response.data.length
    });

  } catch (error) {
    console.error('Recommendation error:', error.message);

    if (error.response) {
      // ML service returned an error
      res.status(error.response.status).json({
        success: false,
        error: error.response.data.detail || error.response.data.error || 'ML service error',
        message: error.response.data.message || 'Error from recommendation service'
      });
    } else if (error.code === 'ECONNREFUSED') {
      // ML service is not running
      res.status(503).json({
        success: false,
        error: 'Service unavailable',
        message: 'ML recommendation service is not available. Please ensure it is running.'
      });
    } else if (error.code === 'ETIMEDOUT') {
      res.status(504).json({
        success: false,
        error: 'Request timeout',
        message: 'Recommendation service took too long to respond'
      });
    } else {
      res.status(500).json({
        success: false,
        error: 'Internal server error',
        message: error.message
      });
    }
  }
});

/**
 * Get available courses (paginated)
 */
app.get('/api/courses', async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 100;
    const offset = parseInt(req.query.offset) || 0;

    const response = await axios.get(`${ML_SERVICE_URL}/courses`, {
      params: { limit, offset },
      timeout: 10000
    });

    res.json(response.data);
  } catch (error) {
    console.error('Courses list error:', error.message);
    res.status(500).json({
      error: 'Failed to retrieve courses',
      message: error.message
    });
  }
});

/**
 * Get cluster information
 */
app.get('/api/clusters/:clusterId', async (req, res) => {
  try {
    const clusterId = parseInt(req.params.clusterId);
    
    if (isNaN(clusterId)) {
      return res.status(400).json({
        error: 'Invalid cluster ID',
        message: 'Cluster ID must be a number'
      });
    }

    const response = await axios.get(`${ML_SERVICE_URL}/clusters/${clusterId}`, {
      timeout: 10000
    });

    res.json(response.data);
  } catch (error) {
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else {
      res.status(500).json({
        error: 'Failed to retrieve cluster information',
        message: error.message
      });
    }
  }
});

/**
 * Root endpoint
 */
app.get('/', (req, res) => {
  res.json({
    service: 'Course Recommendation API',
    version: '1.0.0',
    endpoints: {
      health: '/health',
      recommend: 'POST /api/recommend',
      courses: 'GET /api/courses',
      cluster: 'GET /api/clusters/:clusterId'
    }
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({
    error: 'Internal server error',
    message: err.message
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not found',
    message: `Route ${req.method} ${req.path} not found`
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Backend server running on port ${PORT}`);
  console.log(`📡 ML Service URL: ${ML_SERVICE_URL}`);
  console.log(`📍 Health check: http://localhost:${PORT}/health`);
});

module.exports = app;
