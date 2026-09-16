import re
from typing import Dict, List, Tuple

SECTION_KEYWORDS = {
    "CONTACT": [r"contact", r"contact info", r"personal info", r"address"],
    "SUMMARY": [r"summary", r"professional summary", r"executive summary", r"career summary", r"objective", r"career objective", r"profile", r"about me"],
    "EDUCATION": [r"education", r"academic background", r"educational qualifications", r"academics", r"qualifications", r"degrees"],
    "SKILLS": [r"skills", r"technical skills", r"core competencies", r"key skills", r"technologies", r"tools and technologies", r"skills & proficiencies", r"areas of expertise"],
    "EXPERIENCE": [r"experience", r"work experience", r"professional experience", r"employment history", r"work history", r"career history"],
    "PROJECTS": [r"projects", r"academic projects", r"key projects", r"personal projects", r"technical projects"],
    "CERTIFICATIONS": [r"certifications", r"certificates", r"licenses", r"courses", r"training & certifications"],
    "ACHIEVEMENTS": [r"achievements", r"awards", r"honors", r"accomplishments", r"awards & achievements", r"publications"],
    "INTERNSHIPS": [r"internships", r"internship experience", r"practical training"]
}

def detect_sections(text: str) -> Dict[str, str]:
    """
    Divides resume text into structured sections using heading detection.
    Matches headings by looking for short lines with section keywords (often capitalized or followed by colon).
    Returns a dictionary of section names to their text content.
    """
    if not text:
        return {}

    lines = text.split("\n")
    found_headers: List[Tuple[int, str]] = []

    # Compile regex patterns for fast matching
    compiled_patterns = {}
    for canonical_name, aliases in SECTION_KEYWORDS.items():
        pattern_str = r'^(?:' + '|'.join(aliases) + r')(?:\s*[:\-\|]|\s*$)'
        compiled_patterns[canonical_name] = re.compile(pattern_str, re.IGNORECASE)

    # Detect header lines
    for idx, line in enumerate(lines):
        cleaned_line = line.strip()
        # Section headers are typically short (1 to 6 words)
        if not cleaned_line or len(cleaned_line.split()) > 6:
            continue

        # Strip markdown headers or bullet symbols if present
        heading_candidate = re.sub(r'^[#\*\-=\s]+', '', cleaned_line).strip()

        for canonical_name, regex in compiled_patterns.items():
            if regex.match(heading_candidate):
                found_headers.append((idx, canonical_name))
                break

    # If no headers detected, categorize entire text under "GENERAL"
    if not found_headers:
        return {"GENERAL": text.strip()}

    # Extract text slices between header positions
    sections: Dict[str, str] = {}
    
    # Text before the first header is typically CONTACT / INTRO
    first_idx, first_section = found_headers[0]
    if first_idx > 0:
        header_text = "\n".join(lines[:first_idx]).strip()
        if header_text:
            sections["CONTACT"] = header_text

    for i in range(len(found_headers)):
        current_idx, current_name = found_headers[i]
        next_idx = found_headers[i + 1][0] if (i + 1 < len(found_headers)) else len(lines)
        section_lines = lines[current_idx + 1:next_idx]
        section_content = "\n".join(section_lines).strip()
        
        if current_name in sections:
            # Append if duplicate section found
            sections[current_name] += "\n" + section_content
        else:
            sections[current_name] = section_content

    return sections
