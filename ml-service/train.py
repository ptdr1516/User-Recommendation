"""
Model Training Script
Trains KMeans clustering model with optimal k selection via Elbow Method
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import pickle
import os
from preprocessing import CoursePreprocessor


def calculate_elbow_k(X, max_k=15, min_k=2):
    """
    Find optimal k using Elbow Method
    Returns optimal k and inertia values
    """
    inertias = []
    k_range = range(min_k, max_k + 1)
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10, max_iter=300)
        kmeans.fit(X)
        inertias.append(kmeans.inertia_)
    
    # Calculate rate of change (second derivative approximation)
    # Elbow is where the rate of decrease slows significantly
    if len(inertias) < 3:
        optimal_k = min_k + 1
    else:
        # Calculate first differences
        first_diff = np.diff(inertias)
        # Calculate second differences (rate of change of rate of change)
        second_diff = np.diff(first_diff)
        
        # Find where second derivative is maximum (sharpest bend)
        # Add 2 because of double diff indexing
        optimal_k = np.argmax(second_diff) + min_k + 2
        
        # Ensure optimal_k is within bounds
        optimal_k = max(min_k + 1, min(optimal_k, max_k))
    
    return optimal_k, inertias, k_range


def train_model(data_path=None, output_dir='./'):
    """Train clustering model and save artifacts"""
    
    # Determine data path
    if data_path is None:
        # Try relative path first, then absolute
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(script_dir, '..', 'data', 'courses.csv')
        if not os.path.exists(data_path):
            data_path = os.path.join(script_dir, 'data', 'courses.csv')
    
    # Load data
    print("Loading course data...")
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} courses")
    
    # Preprocess
    print("Preprocessing features...")
    preprocessor = CoursePreprocessor()
    X, df_processed = preprocessor.fit_transform(df)
    print(f"Feature matrix shape: {X.shape}")
    
    # Find optimal k
    print("Finding optimal number of clusters...")
    optimal_k, inertias, k_range = calculate_elbow_k(X, max_k=15)
    print(f"Optimal k: {optimal_k}")
    
    # Train final model
    print(f"Training KMeans with k={optimal_k}...")
    kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10, max_iter=300)
    cluster_labels = kmeans.fit_predict(X)
    
    # Calculate evaluation metrics
    silhouette_avg = silhouette_score(X, cluster_labels)
    print(f"Silhouette Score: {silhouette_avg:.4f}")
    
    # Add cluster labels to dataframe
    df_processed['cluster'] = cluster_labels
    
    # Calculate intra-cluster similarity (average cosine similarity within clusters)
    from sklearn.metrics.pairwise import cosine_similarity
    intra_cluster_similarities = []
    for cluster_id in range(optimal_k):
        cluster_mask = cluster_labels == cluster_id
        cluster_data = X[cluster_mask]
        if len(cluster_data) > 1:
            similarities = cosine_similarity(cluster_data)
            # Get upper triangle (excluding diagonal)
            triu_indices = np.triu_indices(len(similarities), k=1)
            intra_cluster_similarities.append(similarities[triu_indices].mean())
    
    avg_intra_cluster_sim = np.mean(intra_cluster_similarities) if intra_cluster_similarities else 0
    print(f"Average Intra-Cluster Similarity: {avg_intra_cluster_sim:.4f}")
    
    # Save model and preprocessor
    print("Saving model artifacts...")
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, 'kmeans_model.pkl'), 'wb') as f:
        pickle.dump(kmeans, f)
    
    preprocessor.save(os.path.join(output_dir, 'preprocessor.pkl'))
    
    # Save processed data with clusters
    df_processed.to_csv(os.path.join(output_dir, 'courses_with_clusters.csv'), index=False)
    
    # Save evaluation metrics
    metrics = {
        'optimal_k': int(optimal_k),
        'silhouette_score': float(silhouette_avg),
        'intra_cluster_similarity': float(avg_intra_cluster_sim),
        'n_samples': int(len(df)),
        'n_features': int(X.shape[1])
    }
    
    with open(os.path.join(output_dir, 'model_metrics.json'), 'w') as f:
        import json
        json.dump(metrics, f, indent=2)
    
    # Plot elbow curve
    plt.figure(figsize=(10, 6))
    plt.plot(k_range, inertias, 'bo-')
    plt.axvline(x=optimal_k, color='r', linestyle='--', label=f'Optimal k={optimal_k}')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('Inertia')
    plt.title('Elbow Method for Optimal k Selection')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'elbow_curve.png'))
    plt.close()
    
    print("\nTraining complete!")
    print(f"Model saved to {output_dir}")
    print(f"\nEvaluation Metrics:")
    print(f"  Optimal k: {optimal_k}")
    print(f"  Silhouette Score: {silhouette_avg:.4f}")
    print(f"  Intra-Cluster Similarity: {avg_intra_cluster_sim:.4f}")
    
    return kmeans, preprocessor, metrics


if __name__ == '__main__':
    train_model()
