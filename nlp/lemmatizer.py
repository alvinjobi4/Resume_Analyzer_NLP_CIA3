import re
from typing import List, Tuple, Set

# Standard English stop words
DEFAULT_STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it",
    "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my",
    "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or",
    "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same",
    "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so",
    "some", "such", "than", "that", "that's", "the", "their", "theirs", "them",
    "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll",
    "they're", "they've", "this", "those", "through", "to", "too", "under",
    "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're",
    "we've", "were", "weren't", "what", "what's", "when", "when's", "where",
    "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with",
    "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've",
    "your", "yours", "yourself", "yourselves"
}

# Technical words that might otherwise collide with short stopwords or single letters
EXCLUDED_FROM_STOPWORDS = {"c", "r", "go", "ai", "ml", "db", "ui", "ux", "qa"}

def get_stopwords() -> Set[str]:
    """Retrieves stopwords from NLTK if available, otherwise uses DEFAULT_STOPWORDS."""
    try:
        from nltk.corpus import stopwords
        try:
            stop_set = set(stopwords.words('english'))
        except LookupError:
            import nltk
            nltk.download('stopwords', quiet=True)
            stop_set = set(stopwords.words('english'))
        return stop_set - EXCLUDED_FROM_STOPWORDS
    except Exception:
        return DEFAULT_STOPWORDS - EXCLUDED_FROM_STOPWORDS

def remove_stopwords(tokens: List[str]) -> List[str]:
    """Filters out English stopwords from token list."""
    stop_set = get_stopwords()
    return [t for t in tokens if t.lower() not in stop_set and len(t) > 0]

def lemmatize_tokens(tokens: List[str]) -> List[str]:
    """
    Lemmatizes token list using NLTK WordNetLemmatizer or heuristic suffix rules.
    Example: developing -> develop, models -> model.
    """
    if not tokens:
        return []

    try:
        from nltk.stem import WordNetLemmatizer
        try:
            lemmatizer = WordNetLemmatizer()
            # Test one call to ensure wordnet is downloaded
            _ = lemmatizer.lemmatize("testing")
        except LookupError:
            import nltk
            nltk.download('wordnet', quiet=True)
            nltk.download('omw-1.4', quiet=True)
            lemmatizer = WordNetLemmatizer()

        result = []
        for t in tokens:
            # Lemmatize both as verb and noun to get root form
            lemma_v = lemmatizer.lemmatize(t, pos='v')
            lemma = lemmatizer.lemmatize(lemma_v, pos='n')
            result.append(lemma)
        return result
    except Exception:
        # Fallback simple rule-based stem/lemmatizer for common verbal/noun suffixes
        result = []
        for t in tokens:
            word = t
            if word.endswith("ies") and len(word) > 4:
                word = word[:-3] + "y"
            elif word.endswith("ing") and len(word) > 4:
                word = word[:-3]
            elif word.endswith("ed") and len(word) > 3:
                word = word[:-2]
            elif word.endswith("s") and not word.endswith("ss") and len(word) > 3:
                word = word[:-1]
            result.append(word)
        return result

def preprocess_and_lemmatize(tokens: List[str]) -> Tuple[List[str], List[str]]:
    """
    Full pipeline step: takes raw tokens, removes stopwords, then lemmatizes.
    Returns (filtered_tokens, lemmatized_tokens).
    """
    no_stops = remove_stopwords(tokens)
    lemmas = lemmatize_tokens(no_stops)
    return no_stops, lemmas
