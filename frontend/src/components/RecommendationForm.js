import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './RecommendationForm.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001';

function RecommendationForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    preferred_difficulty: '',
    liked_courses: [],
    preferred_organizations: [],
    limit: 10,
    rating_bias: 0.1
  });

  const [courseOptions, setCourseOptions] = useState([]);
  const [organizationOptions, setOrganizationOptions] = useState([]);
  const [loadingCourses, setLoadingCourses] = useState(false);
  const [courseInput, setCourseInput] = useState('');
  const [orgInput, setOrgInput] = useState('');

  useEffect(() => {
    // Load available courses and organizations
    loadOptions();
  }, []);

  const loadOptions = async () => {
    setLoadingCourses(true);
    try {
      const response = await axios.get(`${API_URL}/api/courses`, {
        params: { limit: 1000 }
      });
      
      if (response.data.courses) {
        const courses = response.data.courses;
        setCourseOptions(courses.map(c => c.course_title));
        
        // Extract unique organizations
        const orgs = [...new Set(courses.map(c => c.course_organization))];
        setOrganizationOptions(orgs);
      }
    } catch (error) {
      console.error('Failed to load options:', error);
    } finally {
      setLoadingCourses(false);
    }
  };

  const handleDifficultyChange = (e) => {
    setFormData({ ...formData, preferred_difficulty: e.target.value });
  };

  const handleLimitChange = (e) => {
    const limit = parseInt(e.target.value) || 10;
    setFormData({ ...formData, limit: Math.max(1, Math.min(50, limit)) });
  };

  const handleRatingBiasChange = (e) => {
    const bias = parseFloat(e.target.value) || 0.1;
    setFormData({ ...formData, rating_bias: Math.max(0, Math.min(1, bias)) });
  };

  const addCourse = () => {
    if (courseInput.trim() && !formData.liked_courses.includes(courseInput.trim())) {
      setFormData({
        ...formData,
        liked_courses: [...formData.liked_courses, courseInput.trim()]
      });
      setCourseInput('');
    }
  };

  const removeCourse = (course) => {
    setFormData({
      ...formData,
      liked_courses: formData.liked_courses.filter(c => c !== course)
    });
  };

  const addOrganization = () => {
    if (orgInput.trim() && !formData.preferred_organizations.includes(orgInput.trim())) {
      setFormData({
        ...formData,
        preferred_organizations: [...formData.preferred_organizations, orgInput.trim()]
      });
      setOrgInput('');
    }
  };

  const removeOrganization = (org) => {
    setFormData({
      ...formData,
      preferred_organizations: formData.preferred_organizations.filter(o => o !== org)
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const submitData = {
      preferred_difficulty: formData.preferred_difficulty || null,
      liked_courses: formData.liked_courses,
      preferred_organizations: formData.preferred_organizations,
      limit: formData.limit,
      rating_bias: formData.rating_bias
    };
    
    onSubmit(submitData);
  };

  const filteredCourses = courseOptions.filter(course =>
    course.toLowerCase().includes(courseInput.toLowerCase())
  ).slice(0, 10);

  const filteredOrgs = organizationOptions.filter(org =>
    org.toLowerCase().includes(orgInput.toLowerCase())
  ).slice(0, 10);

  return (
    <form className="recommendation-form" onSubmit={handleSubmit}>
      <div className="form-section">
        <label htmlFor="difficulty">Preferred Difficulty Level</label>
        <select
          id="difficulty"
          value={formData.preferred_difficulty}
          onChange={handleDifficultyChange}
        >
          <option value="">Any Difficulty</option>
          <option value="Beginner">Beginner</option>
          <option value="Intermediate">Intermediate</option>
          <option value="Advanced">Advanced</option>
          <option value="Mixed">Mixed</option>
        </select>
      </div>

      <div className="form-section">
        <label>Liked Courses (Optional)</label>
        <div className="input-with-suggestions">
          <input
            type="text"
            value={courseInput}
            onChange={(e) => setCourseInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addCourse())}
            placeholder="Type course name and press Enter or click Add"
            list="course-suggestions"
          />
          <datalist id="course-suggestions">
            {filteredCourses.map((course, idx) => (
              <option key={idx} value={course} />
            ))}
          </datalist>
          <button type="button" onClick={addCourse} className="add-button">
            Add
          </button>
        </div>
        {formData.liked_courses.length > 0 && (
          <div className="tag-list">
            {formData.liked_courses.map((course, idx) => (
              <span key={idx} className="tag">
                {course}
                <button
                  type="button"
                  onClick={() => removeCourse(course)}
                  className="tag-remove"
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        )}
      </div>

      <div className="form-section">
        <label>Preferred Organizations (Optional)</label>
        <div className="input-with-suggestions">
          <input
            type="text"
            value={orgInput}
            onChange={(e) => setOrgInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addOrganization())}
            placeholder="Type organization name and press Enter or click Add"
            list="org-suggestions"
          />
          <datalist id="org-suggestions">
            {filteredOrgs.map((org, idx) => (
              <option key={idx} value={org} />
            ))}
          </datalist>
          <button type="button" onClick={addOrganization} className="add-button">
            Add
          </button>
        </div>
        {formData.preferred_organizations.length > 0 && (
          <div className="tag-list">
            {formData.preferred_organizations.map((org, idx) => (
              <span key={idx} className="tag">
                {org}
                <button
                  type="button"
                  onClick={() => removeOrganization(org)}
                  className="tag-remove"
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        )}
      </div>

      <div className="form-row">
        <div className="form-section">
          <label htmlFor="limit">Number of Recommendations</label>
          <input
            id="limit"
            type="number"
            min="1"
            max="50"
            value={formData.limit}
            onChange={handleLimitChange}
          />
        </div>

        <div className="form-section">
          <label htmlFor="rating-bias">Rating Preference Weight</label>
          <input
            id="rating-bias"
            type="number"
            min="0"
            max="1"
            step="0.1"
            value={formData.rating_bias}
            onChange={handleRatingBiasChange}
          />
          <small>Higher values prioritize highly-rated courses</small>
        </div>
      </div>

      <button type="submit" className="submit-button" disabled={loadingCourses}>
        {loadingCourses ? 'Loading...' : 'Get Recommendations'}
      </button>
    </form>
  );
}

export default RecommendationForm;
