"""
Feature Engineering and Preprocessing Module
Handles encoding, normalization, and feature matrix creation
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import pickle
import os


class CoursePreprocessor:
    """Handles all preprocessing steps for course data"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.tfidf_vectorizer = TfidfVectorizer(max_features=50, stop_words='english')
        self.feature_names = []
        self.is_fitted = False
        
    def _normalize_enrollment(self, enrollment_str):
        """Convert enrollment strings like '1.2M' to numeric values"""
        if pd.isna(enrollment_str):
            return 0
        
        enrollment_str = str(enrollment_str).strip().upper()
        
        # Extract number and multiplier
        match = re.search(r'([\d.]+)\s*([KM]?)', enrollment_str)
        if not match:
            return 0
        
        number = float(match.group(1))
        multiplier = match.group(2)
        
        if multiplier == 'M':
            return number * 1_000_000
        elif multiplier == 'K':
            return number * 1_000
        else:
            return number
    
    def _encode_difficulty(self, difficulty):
        """Convert difficulty to ordinal scale"""
        difficulty_map = {
            'Beginner': 1,
            'Intermediate': 2,
            'Advanced': 3,
            'Mixed': 2.5
        }
        return difficulty_map.get(str(difficulty).strip(), 2)
    
    def fit_transform(self, df):
        """Fit preprocessor and transform data"""
        # Normalize enrollment
        df['enrollment_numeric'] = df['course_students_enrolled'].apply(
            self._normalize_enrollment
        )
        
        # Encode difficulty
        df['difficulty_encoded'] = df['course_difficulty'].apply(
            self._encode_difficulty
        )
        
        # One-hot encode organizations
        org_dummies = pd.get_dummies(df['course_organization'], prefix='org')
        
        # One-hot encode certificate types
        cert_dummies = pd.get_dummies(df['course_Certificate_type'], prefix='cert')
        
        # TF-IDF on course titles for semantic similarity
        title_features = self.tfidf_vectorizer.fit_transform(
            df['course_title'].fillna('')
        ).toarray()
        title_feature_names = [
            f'title_tfidf_{i}' for i in range(title_features.shape[1])
        ]
        
        # Normalize numeric features
        numeric_features = df[['course_rating', 'enrollment_numeric', 'difficulty_encoded']].values
        numeric_features_scaled = self.scaler.fit_transform(numeric_features)
        
        # Combine all features
        feature_matrix = np.hstack([
            numeric_features_scaled,
            org_dummies.values,
            cert_dummies.values,
            title_features
        ])
        
        # Store feature names for interpretability
        self.feature_names = (
            ['rating_scaled', 'enrollment_scaled', 'difficulty_scaled'] +
            list(org_dummies.columns) +
            list(cert_dummies.columns) +
            title_feature_names
        )
        
        self.is_fitted = True
        
        return feature_matrix, df
    
    def transform(self, df):
        """Transform new data using fitted preprocessor"""
        if not self.is_fitted:
            raise ValueError("Preprocessor must be fitted before transform")
        
        # Normalize enrollment
        df['enrollment_numeric'] = df['course_students_enrolled'].apply(
            self._normalize_enrollment
        )
        
        # Encode difficulty
        df['difficulty_encoded'] = df['course_difficulty'].apply(
            self._encode_difficulty
        )
        
        # One-hot encode organizations (align with training data)
        org_dummies = pd.get_dummies(df['course_organization'], prefix='org')
        # Reindex to match training columns
        org_cols = [col for col in self.feature_names if col.startswith('org_')]
        for col in org_cols:
            if col not in org_dummies.columns:
                org_dummies[col] = 0
        org_dummies = org_dummies.reindex(columns=org_cols, fill_value=0)
        
        # One-hot encode certificate types
        cert_dummies = pd.get_dummies(df['course_Certificate_type'], prefix='cert')
        cert_cols = [col for col in self.feature_names if col.startswith('cert_')]
        for col in cert_cols:
            if col not in cert_dummies.columns:
                cert_dummies[col] = 0
        cert_dummies = cert_dummies.reindex(columns=cert_cols, fill_value=0)
        
        # TF-IDF on course titles
        title_features = self.tfidf_vectorizer.transform(
            df['course_title'].fillna('')
        ).toarray()
        
        # Normalize numeric features
        numeric_features = df[['course_rating', 'enrollment_numeric', 'difficulty_encoded']].values
        numeric_features_scaled = self.scaler.transform(numeric_features)
        
        # Combine all features
        feature_matrix = np.hstack([
            numeric_features_scaled,
            org_dummies.values,
            cert_dummies.values,
            title_features
        ])
        
        return feature_matrix, df
    
    def save(self, filepath):
        """Save preprocessor to disk"""
        with open(filepath, 'wb') as f:
            pickle.dump({
                'scaler': self.scaler,
                'tfidf_vectorizer': self.tfidf_vectorizer,
                'feature_names': self.feature_names,
                'is_fitted': self.is_fitted
            }, f)
    
    @classmethod
    def load(cls, filepath):
        """Load preprocessor from disk"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        preprocessor = cls()
        preprocessor.scaler = data['scaler']
        preprocessor.tfidf_vectorizer = data['tfidf_vectorizer']
        preprocessor.feature_names = data['feature_names']
        preprocessor.is_fitted = data['is_fitted']
        
        return preprocessor
