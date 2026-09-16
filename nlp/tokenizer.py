import re
from typing import List
from .preprocessing import protect_technical_tokens, restore_technical_tokens

def tokenize_words(text: str, lowercase: bool = True) -> List[str]:
    """
    Tokenizes text into words using NLTK word_tokenize or robust regex.
    Protects technical tokens like C++, C#, .NET so they remain intact tokens.
    """
    if not text:
        return []

    # Protect technical keywords
    protected = protect_technical_tokens(text)
    if lowercase:
        protected = protected.lower()

    tokens = []
    try:
        import nltk
        try:
            tokens = nltk.word_tokenize(protected)
        except LookupError:
            nltk.download('punkt', quiet=True)
            nltk.download('punkt_tab', quiet=True)
            tokens = nltk.word_tokenize(protected)
    except Exception:
        # Fallback regex tokenizer that keeps words, hyphens, and placeholders
        tokens = re.findall(r'[a-zA-Z0-9_]+|[^\s\w]', protected)

    # Clean punctuation tokens and restore protected technical tokens
    result = []
    for t in tokens:
        # Filter purely standalone punctuation unless it's a protected token
        if re.match(r'^[\w\-]+$', t) or any(placeholder in t.lower() for placeholder in ["cpp_token", "csharp_token", "dotnet_token", "nodejs_token", "vuejs_token", "reactjs_token"]):
            restored = restore_technical_tokens(t)
            result.append(restored)

    return result

def tokenize_sentences(text: str) -> List[str]:
    """
    Splits text into sentences using NLTK or regex boundary detection.
    """
    if not text:
        return []

    try:
        import nltk
        try:
            return nltk.sent_tokenize(text)
        except LookupError:
            nltk.download('punkt', quiet=True)
            nltk.download('punkt_tab', quiet=True)
            return nltk.sent_tokenize(text)
    except Exception:
        # Regex sentence split
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9])', text)
        return [s.strip() for s in sentences if s.strip()]
