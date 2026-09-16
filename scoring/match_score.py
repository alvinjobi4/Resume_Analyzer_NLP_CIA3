from typing import Dict, List, Any, Tuple
try:
    from config.settings import TFIDF_WEIGHT, SKILL_WEIGHT, REQUIREMENT_WEIGHT, SCORE_CATEGORIES
except (ImportError, ValueError):
    from ..config.settings import TFIDF_WEIGHT, SKILL_WEIGHT, REQUIREMENT_WEIGHT, SCORE_CATEGORIES

def evaluate_education_match(candidate_education: List[str], job_edu_requirement: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compares candidate education credentials with job degree requirements.
    """
    req_degrees = job_edu_requirement.get("degree_levels", [])
    if not req_degrees or job_edu_requirement.get("text") == "Not clearly specified":
        return {
            "score": 100.0,
            "status": "Likely Meets Requirement",
            "badge": "✓ Likely Match",
            "message": "No strict degree level specified by employer, or standard qualification assumed."
        }

    cand_text = " ".join(candidate_education).lower()
    
    # Check if candidate degree matches or exceeds
    has_phd = any(k in cand_text for k in ["ph.d", "doctorate", "doctoral"])
    has_masters = any(k in cand_text for k in ["master", "m.tech", "m.s", "m.sc", "mca", "mba"])
    has_bachelors = any(k in cand_text for k in ["bachelor", "b.tech", "b.e", "b.s", "b.sc", "bca"])

    req_text = " ".join(req_degrees).lower()
    
    if "doctorate" in req_text:
        if has_phd:
            return {"score": 100.0, "status": "Meets Requirement", "badge": "✓ Full Match", "message": "Candidate holds a Doctorate/Ph.D."}
        elif has_masters:
            return {"score": 60.0, "status": "Partial Match", "badge": "⚠ Below Ph.D.", "message": "Employer requests Doctorate; candidate holds Master's."}
        else:
            return {"score": 30.0, "status": "Likely Below Requirement", "badge": "✗ Gap Detected", "message": "Doctorate degree typically required."}

    if "master" in req_text:
        if has_phd or has_masters:
            return {"score": 100.0, "status": "Meets Requirement", "badge": "✓ Full Match", "message": "Candidate holds required Master's/Graduate degree."}
        elif has_bachelors:
            return {"score": 70.0, "status": "Close Match", "badge": "⚠ Bachelor's Detected", "message": "Employer prefers Master's; candidate holds Bachelor's."}
        else:
            return {"score": 40.0, "status": "Ambiguous Match", "badge": "⚠ Not clearly detected", "message": "Master's degree requirement not clearly documented in resume."}

    if "bachelor" in req_text:
        if has_phd or has_masters or has_bachelors:
            return {"score": 100.0, "status": "Meets Requirement", "badge": "✓ Likely Match", "message": "Candidate satisfies the Bachelor's degree qualification."}
        else:
            return {"score": 50.0, "status": "Ambiguous Match", "badge": "⚠ Not clearly detected", "message": "Bachelor's qualification not explicitly detected in resume."}

    return {"score": 75.0, "status": "Likely Satisfied", "badge": "✓ Likely Match", "message": "Educational background appears compatible."}

def evaluate_experience_match(candidate_years: int, job_exp_requirement: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compares candidate estimated experience against job experience requirement.
    """
    min_req = job_exp_requirement.get("min_years", 0)
    req_text = job_exp_requirement.get("text", "Not specified")

    if min_req == 0:
        return {
            "score": 100.0,
            "status": "Requirement Satisfied",
            "badge": "✓ Meets requirement",
            "message": "No minimum years of experience strictly required or entry-level friendly."
        }

    if candidate_years >= min_req:
        return {
            "score": 100.0,
            "status": "Exceeds or Meets Requirement",
            "badge": "✓ Meets requirement",
            "message": f"Candidate experience (~{candidate_years} yrs) satisfies required {req_text}."
        }
    elif candidate_years > 0 and (candidate_years + 1) >= min_req:
        return {
            "score": 75.0,
            "status": "Close to Requirement",
            "badge": "⚠ Close match",
            "message": f"Candidate experience (~{candidate_years} yrs) is near required {req_text}."
        }
    elif candidate_years > 0:
        return {
            "score": 40.0,
            "status": "Below Stated Requirement",
            "badge": "⚠ Requirement may not be fully met",
            "message": f"Job requests {req_text}; resume documents approx {candidate_years} years."
        }
    else:
        return {
            "score": 50.0,
            "status": "Not Clearly Detected",
            "badge": "⚠ Experience years not clearly detected",
            "message": f"Job requests {req_text}. Explicit years of experience not clearly detected on resume."
        }

def get_match_category(score: float) -> Tuple[str, str]:
    """Returns the descriptive category and color code for a given final score."""
    for min_score, max_score, label, color in SCORE_CATEGORIES:
        if min_score <= round(score) <= max_score:
            return label, color
    return "Poor Match", "#ef4444"

def compute_overall_match(
    resume_skills: List[str],
    job_skills: List[str],
    tfidf_similarity_percentage: float,
    candidate_education: List[str],
    job_education: Dict[str, Any],
    candidate_years: int,
    job_experience: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Computes the transparent weighted match score:
    - 50% TF-IDF / Cosine Similarity
    - 40% Skill Match percentage
    - 10% Requirements Match (Education + Experience)
    """
    resume_skills_set = set(resume_skills)
    job_skills_set = set(job_skills)

    # 1. Skill Matching
    matching_skills = sorted(list(resume_skills_set.intersection(job_skills_set)))
    missing_skills = sorted(list(job_skills_set.difference(resume_skills_set)))
    extra_candidate_skills = sorted(list(resume_skills_set.difference(job_skills_set)))

    if len(job_skills) > 0:
        skill_score = (len(matching_skills) / len(job_skills)) * 100.0
    else:
        # If job has no recognized technical skills from list, fallback to TF-IDF score
        skill_score = tfidf_similarity_percentage

    # 2. Education & Experience Evaluation
    edu_match = evaluate_education_match(candidate_education, job_education)
    exp_match = evaluate_experience_match(candidate_years, job_experience)
    requirement_score = (edu_match["score"] * 0.5) + (exp_match["score"] * 0.5)

    # 3. Weighted Final Score
    overall_score = (
        (tfidf_similarity_percentage * TFIDF_WEIGHT) +
        (skill_score * SKILL_WEIGHT) +
        (requirement_score * REQUIREMENT_WEIGHT)
    )
    overall_score = max(0.0, min(100.0, overall_score))
    overall_score = round(overall_score, 1)

    category_label, category_color = get_match_category(overall_score)

    return {
        "overall_score": overall_score,
        "category": category_label,
        "category_color": category_color,
        "score_breakdown": {
            "tfidf_similarity": round(tfidf_similarity_percentage, 1),
            "tfidf_weight": TFIDF_WEIGHT,
            "skill_match": round(skill_score, 1),
            "skill_weight": SKILL_WEIGHT,
            "requirement_match": round(requirement_score, 1),
            "requirement_weight": REQUIREMENT_WEIGHT
        },
        "skills_analysis": {
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "extra_candidate_skills": extra_candidate_skills,
            "total_job_skills_count": len(job_skills),
            "total_matched_skills_count": len(matching_skills),
            "total_missing_skills_count": len(missing_skills)
        },
        "education_match": edu_match,
        "experience_match": exp_match
    }
