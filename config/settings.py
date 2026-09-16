import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
load_dotenv(dotenv_path=BASE_DIR / ".env")

# API Configuration
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "jsearch.p.rapidapi.com")
JSEARCH_ENDPOINT = f"https://{RAPIDAPI_HOST}/search-v2"

# NLP & Scoring Weights (Configurable)
TFIDF_WEIGHT = 0.50
SKILL_WEIGHT = 0.40
REQUIREMENT_WEIGHT = 0.10

# Score Categorization Tiers
SCORE_CATEGORIES = [
    (90, 100, "Excellent Match", "#10b981"),  # Emerald
    (75, 89, "Strong Match", "#3b82f6"),     # Blue
    (60, 74, "Moderate Match", "#f59e0b"),   # Amber
    (40, 59, "Weak Match", "#f97316"),       # Orange
    (0, 39, "Poor Match", "#ef4444"),        # Red
]

# Skills Configuration Path
SKILLS_FILE_PATH = BASE_DIR / "config" / "skills.json"

# SpaCy model configuration
SPACY_MODEL_NAME = "en_core_web_sm"
