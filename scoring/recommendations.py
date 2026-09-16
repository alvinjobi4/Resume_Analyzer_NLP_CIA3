from typing import List, Dict, Any

SKILL_ACTION_GUIDANCE = {
    "Docker": "Containerize an existing project using Docker and write a multi-stage Dockerfile to showcase deployment skills.",
    "Kubernetes": "Demonstrate basic cluster orchestration by creating Helm charts or deploying a service to Minikube/K8s.",
    "AWS": "Build a hands-on project utilizing core AWS services such as S3, EC2, Lambda, or SageMaker and document it on GitHub.",
    "Azure": "Highlight any Microsoft Azure experience or build an Azure Blob/App Service deployment.",
    "PyTorch": "Implement a deep learning computer vision or NLP model using PyTorch and publish the training pipeline.",
    "TensorFlow": "Showcase end-to-end model training and export using TensorFlow / Keras.",
    "Scikit-learn": "Highlight classical machine learning pipelines, cross-validation, and hyperparameter tuning using Scikit-learn.",
    "SQL": "Document complex SQL queries (joins, window functions, indexing) or schema designs in your projects.",
    "PostgreSQL": "Detail relational database schema design, indexing strategies, or ORM usage with PostgreSQL.",
    "MongoDB": "Showcase document-based NoSQL database integration and query optimization with MongoDB.",
    "FastAPI": "Develop and expose an asynchronous RESTful API with automated Swagger docs using FastAPI.",
    "React": "Build an interactive web frontend or dashboard integrating backend REST/GraphQL APIs.",
    "CI/CD": "Set up GitHub Actions or GitLab CI to automate testing and deployment workflows."
}

def generate_recommendations(match_result: Dict[str, Any], job_title: str) -> List[Dict[str, str]]:
    """
    Generates targeted, actionable recommendations based strictly on:
    - Missing skills
    - Experience gap
    - Education alignment
    - TF-IDF document similarity
    """
    recommendations = []
    skills_data = match_result.get("skills_analysis", {})
    missing_skills = skills_data.get("missing_skills", [])
    matching_skills = skills_data.get("matching_skills", [])

    # 1. Skill-specific recommendations
    if missing_skills:
        for skill in missing_skills[:4]:
            guidance = SKILL_ACTION_GUIDANCE.get(
                skill,
                f"Gain hands-on familiarity with {skill} and add a dedicated project or bullet point demonstrating its application."
            )
            recommendations.append({
                "type": "Skill Gap",
                "priority": "High",
                "skill": skill,
                "recommendation": f"Add **{skill}** to your resume.",
                "action": guidance
            })

    # 2. Experience recommendations
    exp_match = match_result.get("experience_match", {})
    if exp_match.get("score", 100) < 80:
        recommendations.append({
            "type": "Experience Alignment",
            "priority": "Medium",
            "skill": "Experience Level",
            "recommendation": "Elaborate on hands-on project timelines or internship contributions.",
            "action": (
                "If you have academic projects, freelance work, or open-source contributions, format them with explicit dates "
                "and quantified outcomes to bridge the documented experience gap."
            )
        })

    # 3. TF-IDF / Keyword Alignment recommendations
    tfidf_score = match_result.get("score_breakdown", {}).get("tfidf_similarity", 0)
    if tfidf_score < 65.0:
        recommendations.append({
            "type": "Content Optimization",
            "priority": "Medium",
            "skill": "Resume Vocabulary",
            "recommendation": f"Incorporate industry keywords from the {job_title} job description into your project descriptions.",
            "action": (
                "Your TF-IDF similarity can improve by tailoring your project descriptions to reflect terminology used by the employer "
                "(e.g., 'model deployment', 'pipeline orchestration', 'latency optimization')."
            )
        })

    # 4. Strengths preservation
    if matching_skills:
        recommendations.append({
            "type": "Highlight Strengths",
            "priority": "Low",
            "skill": ", ".join(matching_skills[:3]),
            "recommendation": f"Prominently showcase your proven skills in {', '.join(matching_skills[:3])}.",
            "action": "Ensure these matching core strengths appear at the top of your resume and in your summary section."
        })

    return recommendations
