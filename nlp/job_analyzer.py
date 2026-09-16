import re
from typing import Dict, List, Any
from .preprocessing import clean_text
from .tokenizer import tokenize_words, tokenize_sentences
from .lemmatizer import preprocess_and_lemmatize
from .skill_extractor import extract_skills

# Common degree keywords in job postings
EDUCATION_PATTERNS = [
    (r"\b(?:ph\.?d|doctorate|doctoral)\b", "Doctorate / Ph.D."),
    (r"\b(?:master'?s?|m\.?tech|m\.?s|m\.?sc|mca|mba)\b", "Master's Degree"),
    (r"\b(?:bachelor'?s?|b\.?tech|b\.?e|b\.?s|b\.?sc|bca)\b", "Bachelor's Degree"),
    (r"\b(?:diploma|associate'?s?)\b", "Associate / Diploma")
]

FIELD_PATTERNS = [
    r"computer science", r"information technology", r"data science",
    r"software engineering", r"electrical engineering", r"mathematics",
    r"statistics", r"related field", r"quantitative field"
]

def extract_experience_requirement(text: str) -> Dict[str, Any]:
    """
    Extracts required years of experience from job descriptions.
    Matches patterns like '3+ years', '2-5 years of experience', 'minimum 4 years'.
    """
    exp_info = {
        "min_years": 0,
        "max_years": 0,
        "raw_matches": [],
        "text": "Not specified"
    }

    patterns = [
        r'(?:minimum|at least)\s+(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)',
        r'(\d+)\s*(?:to|-)\s*(\d+)\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp)',
        r'(\d+)\+\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp)?',
        r'(\d+)\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp)'
    ]

    found_years = []
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for m in matches:
            full_match = m.group(0)
            exp_info["raw_matches"].append(full_match)
            groups = m.groups()
            if groups[0]:
                y1 = int(groups[0])
                # Filter out crazy numbers like '2023 years' or '30 years'
                if 1 <= y1 <= 20:
                    found_years.append(y1)
            if len(groups) > 1 and groups[1]:
                y2 = int(groups[1])
                if 1 <= y2 <= 20:
                    found_years.append(y2)

    if found_years:
        exp_info["min_years"] = min(found_years)
        exp_info["max_years"] = max(found_years)
        if exp_info["min_years"] == exp_info["max_years"]:
            exp_info["text"] = f"{exp_info['min_years']}+ years"
        else:
            exp_info["text"] = f"{exp_info['min_years']}-{exp_info['max_years']} years"

    return exp_info

def extract_education_requirement(text: str) -> Dict[str, Any]:
    """
    Extracts required education level and field of study from job descriptions.
    """
    edu_info = {
        "degree_levels": [],
        "fields": [],
        "raw_matches": [],
        "text": "Not clearly specified"
    }

    for pattern, label in EDUCATION_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if label not in edu_info["degree_levels"]:
                edu_info["degree_levels"].append(label)
                edu_info["raw_matches"].append(match.group(0))

    for pattern in FIELD_PATTERNS:
        match = re.search(r'\b' + pattern + r'\b', text, re.IGNORECASE)
        if match:
            field_name = match.group(0).title()
            if field_name not in edu_info["fields"]:
                edu_info["fields"].append(field_name)

    if edu_info["degree_levels"]:
        degrees_str = " or ".join(edu_info["degree_levels"])
        if edu_info["fields"]:
            edu_info["text"] = f"{degrees_str} in {', '.join(edu_info['fields'][:2])}"
        else:
            edu_info["text"] = degrees_str

    return edu_info

def extract_key_requirements(text: str) -> List[str]:
    """
    Extracts sentences or bullet points that outline critical job requirements.
    """
    sentences = tokenize_sentences(text)
    req_sentences = []
    keywords = ["require", "qualification", "must have", "proficiency", "experience in", "responsible for", "looking for"]

    for s in sentences:
        s_clean = s.strip()
        if any(k in s_clean.lower() for k in keywords) and 15 <= len(s_clean) <= 250:
            req_sentences.append(s_clean)

    return req_sentences[:8]

def analyze_job_description(job_text: str) -> Dict[str, Any]:
    """
    Complete NLP pipeline for a single selected job description:
    Text Cleaning -> Tokenization -> Stopword Removal -> Lemmatization -> Skill & Requirement Extraction
    """
    cleaned = clean_text(job_text)
    tokens = tokenize_words(cleaned)
    no_stops, lemmas = preprocess_and_lemmatize(tokens)

    skills, categorized_skills, skill_matches = extract_skills(cleaned)
    exp_req = extract_experience_requirement(cleaned)
    edu_req = extract_education_requirement(cleaned)
    key_reqs = extract_key_requirements(cleaned)

    return {
        "raw_text": job_text,
        "cleaned_text": cleaned,
        "tokens": tokens,
        "stopwords_removed": no_stops,
        "lemmas": lemmas,
        "skills": skills,
        "categorized_skills": categorized_skills,
        "skill_matches": skill_matches,
        "experience_requirement": exp_req,
        "education_requirement": edu_req,
        "key_requirements": key_reqs
    }
