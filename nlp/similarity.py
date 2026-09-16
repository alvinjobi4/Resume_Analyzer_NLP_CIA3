from typing import Dict, List, Tuple, Any
import numpy as np

def calculate_tfidf_cosine_similarity(
    text1: str,
    text2: str,
    ngram_range: Tuple[int, int] = (1, 2)
) -> Dict[str, Any]:
    """
    Computes genuine TF-IDF vectors and Cosine Similarity between two texts.
    Extracts top keywords and feature weights for transparency and academic demonstration.
    """
    if not text1.strip() or not text2.strip():
        return {
            "similarity_score": 0.0,
            "similarity_percentage": 0.0,
            "common_terms": [],
            "top_resume_terms": [],
            "top_job_terms": [],
            "vocabulary_size": 0
        }

    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        vectorizer = TfidfVectorizer(
            ngram_range=ngram_range,
            stop_words='english',
            sublinear_tf=True
        )

        # Fit and transform both documents
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        feature_names = np.array(vectorizer.get_feature_names_out())

        # Cosine similarity between text1 (resume) and text2 (job)
        sim_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        score = float(sim_matrix[0][0])
        score = max(0.0, min(1.0, score))  # Bound between 0 and 1

        # Extract vector arrays
        v1 = tfidf_matrix[0].toarray()[0]
        v2 = tfidf_matrix[1].toarray()[0]

        # Find top terms in text1
        top_indices1 = np.argsort(v1)[::-1][:10]
        top_resume_terms = [
            {"term": feature_names[i], "weight": round(float(v1[i]), 4)}
            for i in top_indices1 if v1[i] > 0
        ]

        # Find top terms in text2
        top_indices2 = np.argsort(v2)[::-1][:10]
        top_job_terms = [
            {"term": feature_names[i], "weight": round(float(v2[i]), 4)}
            for i in top_indices2 if v2[i] > 0
        ]

        # Find shared terms where both v1 and v2 have positive TF-IDF weight
        shared_mask = (v1 > 0) & (v2 > 0)
        shared_indices = np.where(shared_mask)[0]
        shared_scores = v1[shared_indices] * v2[shared_indices]
        top_shared_indices = shared_indices[np.argsort(shared_scores)[::-1][:10]]

        common_terms = [
            {
                "term": feature_names[i],
                "resume_weight": round(float(v1[i]), 4),
                "job_weight": round(float(v2[i]), 4),
                "combined_impact": round(float(v1[i] * v2[i]), 4)
            }
            for i in top_shared_indices
        ]

        return {
            "similarity_score": score,
            "similarity_percentage": round(score * 100, 2),
            "common_terms": common_terms,
            "top_resume_terms": top_resume_terms,
            "top_job_terms": top_job_terms,
            "vocabulary_size": len(feature_names)
        }

    except Exception as e:
        # Fallback basic Jaccard word similarity if sklearn error occurs
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        jaccard = len(intersection) / len(union) if union else 0.0
        return {
            "similarity_score": jaccard,
            "similarity_percentage": round(jaccard * 100, 2),
            "common_terms": [{"term": w, "resume_weight": 1.0, "job_weight": 1.0, "combined_impact": 1.0} for w in list(intersection)[:10]],
            "top_resume_terms": [],
            "top_job_terms": [],
            "vocabulary_size": len(union)
        }
