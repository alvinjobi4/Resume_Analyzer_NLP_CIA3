import re
from typing import Dict, List, Any, Optional, Tuple, Union
import io

try:
    from parsers.pdf_parser import extract_text_from_pdf
    from parsers.docx_parser import extract_text_from_docx
except (ImportError, ValueError):
    from ..parsers.pdf_parser import extract_text_from_pdf
    from ..parsers.docx_parser import extract_text_from_docx
from .preprocessing import clean_text, extract_contact_info
from .tokenizer import tokenize_words, tokenize_sentences
from .lemmatizer import preprocess_and_lemmatize
from .ner import extract_entities, extract_candidate_name
from .section_detector import detect_sections
from .skill_extractor import extract_skills

def extract_education_details(text: str, sections: Dict[str, str]) -> List[str]:
    """Extracts degree and educational qualifications from resume."""
    edu_text = sections.get("EDUCATION", text)
    degree_patterns = [
        r'\b(?:b\.?\s*tech|bachelor\s+of\s+technology|b\.?\s*e|b\.?\s*s|b\.?\s*sc|bca|bba|bachelor\'?s?)\b[^\n,.]*',
        r'\b(?:m\.?\s*tech|master\s+of\s+technology|m\.?\s*s|m\.?\s*sc|mca|mba|master\'?s?)\b[^\n,.]*',
        r'\b(?:ph\.?\s*d|doctorate)\b[^\n,.]*',
        r'\b(?:diploma|higher\s+secondary|hsc|cbse|icse)\b[^\n,.]*'
    ]

    found = []
    for pat in degree_patterns:
        matches = re.finditer(pat, edu_text, re.IGNORECASE)
        for m in matches:
            deg = m.group(0).strip()
            if len(deg) >= 3 and deg not in found:
                found.append(deg)

    return found if found else ["B.Tech / Bachelor's degree (detected from context)"] if ("computer science" in text.lower() or "engineering" in text.lower()) else []

def estimate_experience_years(text: str, sections: Dict[str, str]) -> Tuple[int, List[str]]:
    """
    Estimates years of professional experience from the resume.
    Looks for explicit statements ('2 years of experience', '3+ yrs') or calculates from date ranges.
    """
    exp_text = sections.get("EXPERIENCE", "") + "\n" + sections.get("SUMMARY", "")
    if not exp_text.strip():
        exp_text = text

    # Check for direct statements like "2 years of experience"
    explicit_matches = re.findall(r'(\d+)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp|software|development)', exp_text, re.IGNORECASE)
    if explicit_matches:
        years = [int(m) for m in explicit_matches if 1 <= int(m) <= 40]
        if years:
            return max(years), [f"{max(years)} years (stated in resume)"]

    # Search for year ranges like 2021 - 2024, 2022 - Present
    date_ranges = re.findall(r'\b(20\d{2}|19\d{2})\s*(?:-|to|–)\s*(20\d{2}|present|current)\b', exp_text, re.IGNORECASE)
    total_span = 0
    current_year = 2026

    for start, end in date_ranges:
        s = int(start)
        e = current_year if end.lower() in ["present", "current"] else int(end)
        if 0 <= (e - s) <= 20:
            total_span += (e - s)

    if total_span > 0:
        capped = min(total_span, 30)
        return capped, [f"Approx. {capped} years (calculated from employment dates)"]

    return 0, []

def analyze_resume(
    file_or_text: Union[str, bytes, io.BytesIO],
    filename: Optional[str] = None
) -> Dict[str, Any]:
    """
    Executes the full Resume NLP Pipeline:
    Text Extraction -> Cleaning -> Tokenization -> Stopword Removal ->
    Lemmatization -> Section Detection -> NER -> Skill Extraction ->
    Candidate Profile Assembly.
    """
    # 1. Text Extraction
    raw_text = ""
    parse_metadata = {}

    if isinstance(file_or_text, str) and not filename:
        # Passed as raw string
        raw_text = file_or_text
        parse_metadata = {"format": "TEXT", "char_count": len(raw_text)}
    else:
        # File path, bytes, or Streamlit UploadedFile
        fn = filename.lower() if filename else (file_or_text if isinstance(file_or_text, str) else "")
        if fn.endswith(".pdf"):
            raw_text, parse_metadata = extract_text_from_pdf(file_or_text)
        elif fn.endswith(".docx"):
            raw_text, parse_metadata = extract_text_from_docx(file_or_text)
        else:
            # Fallback treat as text
            if hasattr(file_or_text, "read"):
                content = file_or_text.read()
                raw_text = content.decode("utf-8", errors="ignore") if isinstance(content, bytes) else str(content)
            elif isinstance(file_or_text, bytes):
                raw_text = file_or_text.decode("utf-8", errors="ignore")
            else:
                raw_text = str(file_or_text)
            parse_metadata = {"format": "TEXT", "char_count": len(raw_text)}

    # 2. Text Cleaning
    cleaned_text = clean_text(raw_text)

    # 3. Tokenization
    tokens = tokenize_words(cleaned_text)

    # 4. Stopword Removal & Lemmatization
    no_stops, lemmas = preprocess_and_lemmatize(tokens)

    # 5. Section Detection
    sections = detect_sections(cleaned_text)

    # 6. Contact Information
    contact_info = extract_contact_info(cleaned_text)

    # 7. Named Entity Recognition
    entities = extract_entities(cleaned_text)
    candidate_name = extract_candidate_name(cleaned_text, entities)

    # 8. Skill Extraction
    skills, categorized_skills, skill_matches = extract_skills(cleaned_text)

    # 9. Education & Experience Extraction
    education_list = extract_education_details(cleaned_text, sections)
    exp_years, exp_details = estimate_experience_years(cleaned_text, sections)

    # Extract Project highlights if PROJECTS section exists
    project_highlights = []
    if "PROJECTS" in sections:
        proj_lines = [l.strip() for l in sections["PROJECTS"].split("\n") if l.strip()]
        project_highlights = proj_lines[:5]

    # Assemble Structured Candidate Profile
    candidate_profile = {
        "name": candidate_name,
        "email": contact_info["email"],
        "phone": contact_info["phone"],
        "linkedin": contact_info["linkedin"],
        "github": contact_info["github"],
        "skills": skills,
        "categorized_skills": categorized_skills,
        "education": education_list if education_list else ["Not detected"],
        "experience_years": exp_years,
        "experience": exp_details if exp_details else ["Not detected"],
        "projects": project_highlights if project_highlights else ["Not detected"],
        "certifications": sections.get("CERTIFICATIONS", "Not detected").split("\n") if "CERTIFICATIONS" in sections else ["Not detected"],
        "organizations": entities.get("ORG", [])[:6],
        "locations": entities.get("GPE", [])[:4]
    }

    # Complete Step-by-Step NLP Trace for Evaluation / Viva
    nlp_trace = {
        "raw_text": raw_text[:2000] + ("..." if len(raw_text) > 2000 else ""),
        "raw_char_count": len(raw_text),
        "cleaned_text": cleaned_text[:2000] + ("..." if len(cleaned_text) > 2000 else ""),
        "total_tokens_count": len(tokens),
        "sample_tokens": tokens[:40],
        "stopwords_removed_count": len(no_stops),
        "sample_stopwords_removed": no_stops[:40],
        "lemmas_count": len(lemmas),
        "sample_lemmas": lemmas[:40],
        "sections_detected": list(sections.keys()),
        "named_entities": {
            "PERSON": entities.get("PERSON", []),
            "ORG": entities.get("ORG", [])[:10],
            "GPE": entities.get("GPE", [])[:10],
            "DATE": entities.get("DATE", [])[:10]
        },
        "extracted_skills_count": len(skills),
        "extracted_skills": skills
    }

    return {
        "raw_text": raw_text,
        "cleaned_text": cleaned_text,
        "candidate_profile": candidate_profile,
        "sections": sections,
        "nlp_trace": nlp_trace,
        "parse_metadata": parse_metadata
    }
