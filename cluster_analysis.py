# cluster_analysis.py
# Unsupervised clustering of journal entries

from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pandas as pd

# ----------------------------
# Custom stopwords for journaling context
# ----------------------------
CUSTOM_STOPWORDS = [
    "like", "im", "dont", "idk", "af",
    "haha", "hahaha", "lol",
    "bit", "guess", "know",
    "yeah", "okay", "ok",
    "really", "just", "hahahaha"
]

def cluster_journals(texts, n_clusters=3):
    """
    Perform TF-IDF + KMeans clustering on journal texts.

    Parameters:
        texts (list of str): Full journal entries
        n_clusters (int): Number of clusters

    Returns:
        labels (list): Cluster label for each journal
        coords_df (DataFrame): 2D coordinates for visualization
        cluster_terms (dict): Top keywords per cluster
    """

    # ----------------------------
    # Vectorize text
    # ----------------------------
    # Remove common English stopwords and journaling fillers
    # to reduce noise while preserving emotional expression

    ALL_STOPWORDS = list(ENGLISH_STOP_WORDS.union(CUSTOM_STOPWORDS))
    
    vectorizer = TfidfVectorizer(
        stop_words = ALL_STOPWORDS,
        max_features = 500
    )
    X = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()

    # ----------------------------
    # KMeans clustering
    # ----------------------------
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X)

    # ----------------------------
    # Extract top terms per cluster
    # ----------------------------
    cluster_terms = {}
    for i in range(n_clusters):
        center = kmeans.cluster_centers_[i]
        top_indices = center.argsort()[-5:][::-1]
        cluster_terms[i] = [feature_names[j] for j in top_indices]

    # ----------------------------
    # Reduce to 2D for visualization
    # ----------------------------
    pca = PCA(n_components=2)
    coords = pca.fit_transform(X.toarray())

    coords_df = pd.DataFrame({
        "x": coords[:, 0],
        "y": coords[:, 1],
        "cluster": labels
    })

    # Add display-friendly cluster index
    coords_df["display_cluster"] = coords_df["cluster"] + 1

    return labels, coords_df, cluster_terms
