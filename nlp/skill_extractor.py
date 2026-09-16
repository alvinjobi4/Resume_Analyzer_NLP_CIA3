import json
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple, Any
try:
    from config.settings import SKILLS_FILE_PATH
except (ImportError, ValueError):
    from ..config.settings import SKILLS_FILE_PATH

# Cache skills dictionary
_SKILLS_CACHE = None

def load_skills_data() -> Dict[str, Any]:
    """Loads skills taxonomy and alias mappings from config/skills.json."""
    global _SKILLS_CACHE
    if _SKILLS_CACHE is not None:
        return _SKILLS_CACHE

    if SKILLS_FILE_PATH.exists():
        with open(SKILLS_FILE_PATH, "r", encoding="utf-8") as f:
            _SKILLS_CACHE = json.load(f)
    else:
        # Fallback minimal dictionary
        _SKILLS_CACHE = {
            "categories": {
                "Programming Languages": ["Python", "Java", "C++", "C#", "JavaScript", "TypeScript", "SQL"],
                "Machine Learning & AI": ["Machine Learning", "Deep Learning", "NLP", "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy"],
                "Cloud & DevOps": ["AWS", "Azure", "Docker", "Kubernetes", "Git"]
            },
            "aliases": {
                "ml": "Machine Learning",
                "sklearn": "Scikit-learn",
                "nlp": "Natural Language Processing"
            }
        }
    return _SKILLS_CACHE

def extract_skills(text: str) -> Tuple[List[str], Dict[str, List[str]], List[Dict[str, str]]]:
    """
    Extracts and canonicalizes technical skills from text.
    Handles multi-word skills, special punctuation (C++, C#, .NET, Node.js), and alias normalization.
    Returns:
    - unique_skills: sorted list of canonical skill names
    - categorized_skills: dict of category -> [skills]
    - match_details: list of {matched_text, canonical_name, category}
    """
    if not text:
        return [], {}, []

    skills_data = load_skills_data()
    categories = skills_data.get("categories", {})
    aliases = skills_data.get("aliases", {})

    # Inverted lookup from canonical skill name to category
    skill_to_category = {}
    canonical_skills: Set[str] = set()
    for cat, skills_list in categories.items():
        for s in skills_list:
            canonical_skills.add(s)
            skill_to_category[s] = cat

    found_skills: Set[str] = set()
    match_details: List[Dict[str, str]] = []

    # Helper for case-insensitive exact boundary match
    def matches_term(term: str, target_text: str) -> bool:
        # Special handling for single-character or punctuated terms
        if term.lower() == "c":
            # Must not be surrounded by letters, pluses, or hashes
            return bool(re.search(r'(?<![a-zA-Z0-9+#])C(?![a-zA-Z0-9+#])', target_text))
        elif term.lower() == "r":
            # Match R programming language: preceded by comma, slash, space, or 'language'
            return bool(re.search(r'(?<![a-zA-Z0-9])R(?=\s+(?:programming|language|scripting)|\s*[,/|\)])', target_text, re.IGNORECASE))
        elif term.lower() in ["c++", "c#", ".net"]:
            pattern = re.escape(term)
            return bool(re.search(r'(?<![a-zA-Z0-9])' + pattern + r'(?![a-zA-Z0-9])', target_text, re.IGNORECASE))
        else:
            pattern = r'\b' + re.escape(term) + r'\b'
            return bool(re.search(pattern, target_text, re.IGNORECASE))

    # 1. Match canonical skills
    for skill in canonical_skills:
        if matches_term(skill, text):
            found_skills.add(skill)
            cat = skill_to_category.get(skill, "General")
            match_details.append({
                "matched_text": skill,
                "canonical_name": skill,
                "category": cat
            })

    # 2. Match aliases (e.g. ML -> Machine Learning, sklearn -> Scikit-learn)
    for alias, canonical_name in aliases.items():
        if matches_term(alias, text):
            found_skills.add(canonical_name)
            cat = skill_to_category.get(canonical_name, "General")
            match_details.append({
                "matched_text": alias,
                "canonical_name": canonical_name,
                "category": cat
            })

    sorted_skills = sorted(list(found_skills))

    # Organize found skills by category
    categorized: Dict[str, List[str]] = {}
    for skill in sorted_skills:
        cat = skill_to_category.get(skill, "Other Technical Skills")
        if cat not in categorized:
            categorized[cat] = []
        categorized[cat].append(skill)

    return sorted_skills, categorized, match_details
