import re
from typing import Dict, List, Any, Optional

# Lazy load spaCy model
_nlp = None

def get_spacy_model():
    """Loads spaCy model once with caching, falls back gracefully if not yet downloaded."""
    global _nlp
    if _nlp is not None:
        return _nlp

    try:
        import spacy
        try:
            _nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Try loading or downloading
            try:
                from spacy.cli import download
                download("en_core_web_sm")
                _nlp = spacy.load("en_core_web_sm")
            except Exception:
                _nlp = None
    except ImportError:
        _nlp = None

    return _nlp

NON_NAME_TERMS = {
    "resume", "curriculum", "vitae", "cv", "profile", "summary",
    "contact", "objective", "experience", "education", "skills",
    "projects", "certifications", "phone", "email", "address",
    "portfolio", "page", "developer", "engineer", "candidate",
    "machine", "learning", "data", "science", "scientist",
    "software", "technologies", "technology", "artificial", "intelligence",
    "deep", "python", "java", "sql", "analyst", "engineering", "vit",
    "university", "college", "institute", "school", "bachelor", "master"
}

def extract_entities(text: str) -> Dict[str, Any]:
    """
    Extracts Named Entities using spaCy NER.
    Returns categorized entities: PERSON, ORG, GPE, DATE, etc.
    """
    nlp = get_spacy_model()
    result = {
        "PERSON": [],
        "ORG": [],
        "GPE": [],
        "DATE": [],
        "raw_entities": []
    }

    if not text:
        return result

    if nlp is not None:
        doc = nlp(text[:50000])
        for ent in doc.ents:
            cleaned_text = ent.text.strip().replace("\n", " ")
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
            if not cleaned_text or len(cleaned_text) < 2:
                continue

            entity_info = {
                "text": cleaned_text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            }
            result["raw_entities"].append(entity_info)

            if ent.label_ in result and cleaned_text not in result[ent.label_]:
                result[ent.label_].append(cleaned_text)
    else:
        date_pattern = r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}|\b(?:19|20)\d{2}\b'
        dates = list(set(re.findall(date_pattern, text, re.IGNORECASE)))
        result["DATE"] = dates[:10]

    return result

def extract_candidate_name(text: str, entities: Optional[Dict[str, Any]] = None) -> str:
    """
    Identifies the candidate's name using header lines and spaCy PERSON entities.
    Prioritizes top document lines (resume title convention) and filters domain buzzwords.
    """
    if not text:
        return "Not detected"

    # Step 1: Top-line heuristic (standard resume format: candidate name is in the first 1-3 lines)
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    for line in lines[:4]:
        # Ignore contact information, URLs, or lines with digits
        if "@" in line or "http" in line or "github" in line or "linkedin" in line or "phone" in line.lower():
            continue
        if re.search(r'\d', line):
            continue
        
        # Clean line
        cleaned_line = re.sub(r'[^a-zA-Z\s\.-]', '', line).strip()
        words = cleaned_line.split()
        if 2 <= len(words) <= 4:
            lower_words = [w.lower() for w in words]
            if not any(w in NON_NAME_TERMS for w in lower_words):
                if all(w[0].isupper() for w in words if w):
                    return cleaned_line

    # Step 2: Check spaCy PERSON entities
    if entities and entities.get("PERSON"):
        for person in entities["PERSON"]:
            cleaned = person.strip().replace("\n", " ")
            cleaned = re.sub(r'[^a-zA-Z\s\.-]', '', cleaned).strip()
            words = cleaned.split()
            if 2 <= len(words) <= 4:
                lower_words = [w.lower() for w in words]
                if not any(w in NON_NAME_TERMS for w in lower_words):
                    pos = text.find(person)
                    if 0 <= pos <= 400:
                        return cleaned

    # Step 3: Check first line even if 1 word or mixed case
    if lines:
        first_line = re.sub(r'[^a-zA-Z\s]', '', lines[0]).strip()
        words = first_line.split()
        if 1 <= len(words) <= 3 and not any(w.lower() in NON_NAME_TERMS for w in words):
            return first_line

    return "Not detected"
