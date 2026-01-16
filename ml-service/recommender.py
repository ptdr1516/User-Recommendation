"""
Recommendation Engine
Implements similarity-based recommendation with clustering and user behavior simulation
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import pickle
import os
from preprocessing import CoursePreprocessor


class CourseRecommender:
    """Main recommendation engine"""
    
    def __init__(self, model_path='./kmeans_model.pkl', 
                 preprocessor_path='./preprocessor.pkl',
                 data_path='./courses_with_clusters.csv'):
        """Initialize recommender with trained model"""
        
        import os
        
        # Resolve paths relative to script directory if needed
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        if not os.path.isabs(model_path):
            model_path = os.path.join(script_dir, model_path)
        if not os.path.isabs(preprocessor_path):
            preprocessor_path = os.path.join(script_dir, preprocessor_path)
        if not os.path.isabs(data_path):
            data_path = os.path.join(script_dir, data_path)
        
        # Load model
        with open(model_path, 'rb') as f:
            self.kmeans_model = pickle.load(f)
        
        # Load preprocessor
        self.preprocessor = CoursePreprocessor.load(preprocessor_path)
        
        # Load course data
        self.courses_df = pd.read_csv(data_path)
        
        # Precompute feature matrix for all courses
        self.feature_matrix, _ = self.preprocessor.transform(self.courses_df)
        
        # Get cluster assignments
        self.courses_df['cluster'] = self.kmeans_model.predict(self.feature_matrix)
    
    def _create_user_profile(self, preferred_difficulty=None, liked_courses=None, 
                            preferred_organizations=None, rating_bias=0.1):
        """
        Create synthetic user profile vector based on preferences
        
        Args:
            preferred_difficulty: 'Beginner', 'Intermediate', 'Advanced', or 'Mixed'
            liked_courses: List of course titles user has liked/viewed
            preferred_organizations: List of preferred organizations
            rating_bias: Weight for rating preference (0-1)
        
        Returns:
            user_profile: Feature vector representing user preferences
        """
        # Start with zero vector matching feature dimensions
        user_profile = np.zeros(self.feature_matrix.shape[1])
        
        # Find courses matching user preferences
        matching_courses = self.courses_df.copy()
        
        # Filter by difficulty if specified
        if preferred_difficulty:
            matching_courses = matching_courses[
                matching_courses['course_difficulty'] == preferred_difficulty
            ]
        
        # Filter by liked courses if specified
        if liked_courses:
            liked_mask = matching_courses['course_title'].isin(liked_courses)
            if liked_mask.any():
                matching_courses = matching_courses[liked_mask]
            else:
                # If exact matches not found, use partial matching
                liked_mask = matching_courses['course_title'].str.contains(
                    '|'.join(liked_courses), case=False, na=False
                )
                if liked_mask.any():
                    matching_courses = matching_courses[liked_mask]
        
        # Filter by organizations if specified
        if preferred_organizations:
            org_mask = matching_courses['course_organization'].isin(preferred_organizations)
            if org_mask.any():
                matching_courses = matching_courses[org_mask]
        
        # If no matching courses, use all courses with preference weighting
        if len(matching_courses) == 0:
            matching_courses = self.courses_df.copy()
            weight = 0.5  # Lower weight if no exact matches
        else:
            weight = 1.0
        
        # Get indices of matching courses
        matching_indices = matching_courses.index.tolist()
        
        # Create user profile as weighted average of matching courses
        if len(matching_indices) > 0:
            matching_features = self.feature_matrix[matching_indices]
            
            # Apply rating-based weighting if rating_bias > 0
            if rating_bias > 0:
                ratings = matching_courses['course_rating'].values
                # Normalize ratings to 0-1 range for weighting
                rating_weights = (ratings - ratings.min()) / (ratings.max() - ratings.min() + 1e-6)
                rating_weights = 1 + rating_bias * rating_weights
                # Apply weights
                matching_features = matching_features * rating_weights.reshape(-1, 1)
            
            # Average the features
            user_profile = matching_features.mean(axis=0) * weight
        
        # Normalize user profile
        profile_norm = np.linalg.norm(user_profile)
        if profile_norm > 0:
            user_profile = user_profile / profile_norm
        
        return user_profile
    
    def recommend(self, preferred_difficulty=None, liked_courses=None,
                  preferred_organizations=None, limit=10, rating_bias=0.1,
                  exclude_courses=None):
        """
        Generate course recommendations
        
        Args:
            preferred_difficulty: User's preferred difficulty level
            liked_courses: List of course titles user has liked
            preferred_organizations: List of preferred organizations
            limit: Number of recommendations to return
            rating_bias: Weight for rating preference
            exclude_courses: List of course titles to exclude from results
        
        Returns:
            List of recommended courses with similarity scores and explanations
        """
        # Create user profile
        user_profile = self._create_user_profile(
            preferred_difficulty=preferred_difficulty,
            liked_courses=liked_courses,
            preferred_organizations=preferred_organizations,
            rating_bias=rating_bias
        )
        
        # Reshape for cosine similarity
        user_profile = user_profile.reshape(1, -1)
        
        # Calculate cosine similarity with all courses
        similarities = cosine_similarity(user_profile, self.feature_matrix)[0]
        
        # Get user's cluster (predict cluster for user profile)
        user_cluster = self.kmeans_model.predict(user_profile)[0]
        
        # Create results dataframe
        results = self.courses_df.copy()
        results['similarity_score'] = similarities
        
        # Boost scores for courses in same cluster
        same_cluster_mask = results['cluster'] == user_cluster
        results.loc[same_cluster_mask, 'similarity_score'] *= 1.2
        
        # Secondary boost for higher ratings and enrollments
        rating_normalized = (results['course_rating'] - results['course_rating'].min()) / \
                           (results['course_rating'].max() - results['course_rating'].min() + 1e-6)
        enrollment_normalized = (results['enrollment_numeric'] - results['enrollment_numeric'].min()) / \
                               (results['enrollment_numeric'].max() - results['enrollment_numeric'].min() + 1e-6)
        
        # Apply boosts (smaller weights to maintain similarity as primary signal)
        results['similarity_score'] += 0.05 * rating_normalized
        results['similarity_score'] += 0.03 * enrollment_normalized
        
        # Exclude specified courses
        if exclude_courses:
            exclude_mask = results['course_title'].isin(exclude_courses)
            results = results[~exclude_mask]
        
        # Exclude already liked courses
        if liked_courses:
            liked_mask = results['course_title'].isin(liked_courses)
            results = results[~liked_mask]
        
        # Sort by similarity score
        results = results.sort_values('similarity_score', ascending=False)
        
        # Get top recommendations
        top_recommendations = results.head(limit)
        
        # Format output
        recommendations = []
        for idx, row in top_recommendations.iterrows():
            # Generate explanation
            explanation_parts = []
            
            if row['cluster'] == user_cluster:
                explanation_parts.append("Same cluster as your preferences")
            
            if preferred_difficulty and row['course_difficulty'] == preferred_difficulty:
                explanation_parts.append(f"Matches your {preferred_difficulty} difficulty preference")
            
            if preferred_organizations and row['course_organization'] in preferred_organizations:
                explanation_parts.append(f"From preferred organization: {row['course_organization']}")
            
            if row['course_rating'] >= 4.5:
                explanation_parts.append("Highly rated course")
            
            if row['enrollment_numeric'] >= 1_000_000:
                explanation_parts.append("Popular course (1M+ enrollments)")
            
            explanation = "; ".join(explanation_parts) if explanation_parts else "Similar content and features"
            
            recommendations.append({
                'course_title': row['course_title'],
                'organization': row['course_organization'],
                'certificate_type': row['course_Certificate_type'],
                'rating': float(row['course_rating']),
                'difficulty': row['course_difficulty'],
                'students_enrolled': str(row['course_students_enrolled']),
                'similarity_score': float(row['similarity_score']),
                'cluster': int(row['cluster']),
                'explanation': explanation
            })
        
        return recommendations
    
    def get_cluster_info(self, cluster_id):
        """Get information about a specific cluster"""
        cluster_courses = self.courses_df[self.courses_df['cluster'] == cluster_id]
        
        return {
            'cluster_id': cluster_id,
            'n_courses': len(cluster_courses),
            'avg_rating': float(cluster_courses['course_rating'].mean()),
            'difficulty_distribution': cluster_courses['course_difficulty'].value_counts().to_dict(),
            'top_organizations': cluster_courses['course_organization'].value_counts().head(5).to_dict(),
            'sample_courses': cluster_courses['course_title'].head(10).tolist()
        }
