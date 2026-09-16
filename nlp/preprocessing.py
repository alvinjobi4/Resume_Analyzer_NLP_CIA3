import re
from typing import Dict, List, Tuple

# Technical terms to protect during punctuation normalization
PROTECTED_TERMS = {
    "c++": "CPP_TOKEN",
    "c#": "CSHARP_TOKEN",
    ".net": "DOTNET_TOKEN",
    "node.js": "NODEJS_TOKEN",
    "vue.js": "VUEJS_TOKEN",
    "react.js": "REACTJS_TOKEN",
    "next.js": "NEXTJS_TOKEN",
    "express.js": "EXPRESSJS_TOKEN",
    "ci/cd": "CICD_TOKEN",
    "tcp/ip": "TCPIP_TOKEN"
}

REVERSE_PROTECTED_TERMS = {v: k for k, v in PROTECTED_TERMS.items()}

def protect_technical_tokens(text: str) -> str:
    """Replaces tokens like C++, C#, .NET with placeholder tokens so regex doesn't mangle them."""
    for term, placeholder in PROTECTED_TERMS.items():
        if term.startswith('.'):
            pattern = r'(?i)(?<!\S)' + re.escape(term) + r'(?!\S)'
        elif term.endswith('+') or term.endswith('#'):
            pattern = r'(?i)(?<!\S)' + re.escape(term) + r'(?!\S)'
        else:
            pattern = r'(?i)\b' + re.escape(term) + r'\b'
        text = re.sub(pattern, placeholder, text)
    return text

def restore_technical_tokens(text: str) -> str:
    """Restores placeholders back to their canonical technical token representation."""
    for placeholder, term in REVERSE_PROTECTED_TERMS.items():
        text = text.replace(placeholder, term)
        text = text.replace(placeholder.lower(), term)
    return text

def clean_text(text: str, keep_technical: bool = True) -> str:
    """
    Cleans raw resume or job text:
    - Normalizes line breaks and whitespace
    - Removes unprintable characters, decorative bullets, and noise
    - Optionally preserves programming tokens (C++, C#, .NET)
    """
    if not text:
        return ""

    if keep_technical:
        text = protect_technical_tokens(text)

    # Normalize carriage returns and line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Replace decorative bullet points and symbols with standard space or newlines
    text = re.sub(r'[\u2022\u2023\u25E6\u2043\u2219\u25CB\u25CF\u25AA\u25A0\u25BA\u27A2\u2713\u2714\u2716\u2717\uF0B7\uF0A7\uF0D8]', ' ', text)

    # Replace tabs and multiple spaces with a single space (while keeping newlines)
    lines = []
    for line in text.split("\n"):
        cleaned_line = re.sub(r'[ \t\f\v]+', ' ', line).strip()
        if cleaned_line:
            lines.append(cleaned_line)
    text = "\n".join(lines)

    # Remove non-ASCII weird control symbols but keep standard punctuation
    text = re.sub(r'[^\x20-\x7E\n]', ' ', text)

    if keep_technical:
        text = restore_technical_tokens(text)

    return text.strip()

def extract_contact_info(text: str) -> Dict[str, str]:
    """
    Extracts email, phone number, and social profiles (LinkedIn, GitHub) from resume text.
    """
    contact = {
        "email": "Not detected",
        "phone": "Not detected",
        "linkedin": "Not detected",
        "github": "Not detected"
    }

    # Email extraction regex
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    if emails:
        contact["email"] = emails[0].strip()

    # Phone number extraction regex (supports international, brackets, dashes, dots)
    phone_pattern = r'(?:(?:\+|00)\d{1,3}[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}|\b\d{10}\b|\b\d{5}[-\s]\d{5}\b'
    phones = re.findall(phone_pattern, text)
    # Filter out year numbers like 2020-2024 or short numbers
    valid_phones = [p.strip() for p in phones if len(re.sub(r'\D', '', p)) >= 10]
    if valid_phones:
        contact["phone"] = valid_phones[0]

    # LinkedIn profile
    linkedin_match = re.search(r'(?:https?://)?(?:www\.)?linkedin\.com/in/([a-zA-Z0-9_-]+)', text, re.IGNORECASE)
    if linkedin_match:
        contact["linkedin"] = f"linkedin.com/in/{linkedin_match.group(1)}"

    # GitHub profile
    github_match = re.search(r'(?:https?://)?(?:www\.)?github\.com/([a-zA-Z0-9_-]+)', text, re.IGNORECASE)
    if github_match:
        contact["github"] = f"github.com/{github_match.group(1)}"

    return contact
