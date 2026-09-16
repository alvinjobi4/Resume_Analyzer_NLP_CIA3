import streamlit as st
import json
from pathlib import Path
try:
    from nlp.resume_analyzer import analyze_resume
except (ImportError, ValueError):
    from ..nlp.resume_analyzer import analyze_resume

def render_resume_page():
    st.markdown('<h1 class="main-title">Resume NLP Extraction</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Upload your resume in <b>PDF</b> or <b>DOCX</b> format. '
        'Candidate information, skills, and sections are automatically extracted using NLP.</p>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a Resume File",
            type=["pdf", "docx"],
            help="Supported formats: PDF, DOCX. The NLP pipeline extracts all attributes automatically."
        )
    with col2:
        st.write("")
        st.write("")
        use_sample = st.button("📄 Load Sample Resume", use_container_width=True, help="Load a pre-configured Machine Learning engineer resume for immediate evaluation.")

    # Handle file upload or sample selection
    if use_sample:
        sample_path = Path(__file__).resolve().parent.parent / "sample_data" / "sample_resume.txt"
        if sample_path.exists():
            with open(sample_path, "r", encoding="utf-8") as f:
                sample_text = f.read()
            with st.spinner("Executing NLP Pipeline on Sample Resume..."):
                analysis = analyze_resume(sample_text)
                st.session_state["resume_data"] = analysis
                st.session_state["resume_filename"] = "sample_resume.txt"
            st.success("✓ Loaded and processed sample resume successfully!")
        else:
            st.error("Sample resume file not found.")

    elif uploaded_file is not None:
        # Avoid redundant re-processing if the file didn't change
        if st.session_state.get("resume_filename") != uploaded_file.name:
            with st.spinner(f"Extracting and processing {uploaded_file.name} with NLP..."):
                try:
                    analysis = analyze_resume(uploaded_file, filename=uploaded_file.name)
                    st.session_state["resume_data"] = analysis
                    st.session_state["resume_filename"] = uploaded_file.name
                    st.success(f"✓ Successfully processed **{uploaded_file.name}**")
                except Exception as e:
                    st.error(f"Error parsing resume: {str(e)}")
                    return

    # Display results if resume is processed
    resume_data = st.session_state.get("resume_data")
    if not resume_data:
        st.info("👋 Upload a resume above or click **'Load Sample Resume'** to get started.")
        return

    profile = resume_data["candidate_profile"]
    trace = resume_data["nlp_trace"]

    # Candidate Profile Header Card
    st.markdown("### 👤 Candidate Profile")
    prof_col1, prof_col2, prof_col3 = st.columns([1.5, 1.5, 1])

    with prof_col1:
        st.markdown(f"**Name:** `{profile['name']}`")
        st.markdown(f"**Email:** `{profile['email']}`")
        st.markdown(f"**Phone:** `{profile['phone']}`")

    with prof_col2:
        st.markdown(f"**LinkedIn:** `{profile['linkedin']}`")
        st.markdown(f"**GitHub:** `{profile['github']}`")
        st.markdown(f"**Experience:** `{profile['experience_years']} years`")

    with prof_col3:
        st.metric("Skills Detected", len(profile["skills"]))
        st.metric("Sections Detected", len(resume_data["sections"]))

    st.divider()

    # Education & Experience Details
    st.markdown("### 🎓 Education & Experience")
    ee_col1, ee_col2 = st.columns(2)
    with ee_col1:
        st.markdown("**Education Qualifications:**")
        for edu in profile["education"]:
            st.markdown(f"- {edu}")
    with ee_col2:
        st.markdown("**Experience Highlights:**")
        for exp in profile["experience"]:
            st.markdown(f"- {exp}")

    st.divider()

    # Extracted Technical Skills
    st.markdown("### 🛠 Extracted Technical Skills")
    if profile["skills"]:
        categorized = profile.get("categorized_skills", {})
        for cat, skills in categorized.items():
            st.markdown(f"**{cat}**")
            badges_html = " ".join([f'<span class="skill-badge skill-neutral">{s}</span>' for s in skills])
            st.markdown(badges_html, unsafe_allow_html=True)
            st.write("")
    else:
        st.warning("No technical skills from the configured dictionary were detected.")

    st.divider()

    # Detected Resume Sections
    with st.expander("📑 Detected Resume Sections & Extracted Text", expanded=False):
        sections = resume_data.get("sections", {})
        for sec_name, sec_content in sections.items():
            st.markdown(f"#### Section: `{sec_name}`")
            st.text(sec_content if sec_content else "No textual content")

    # NLP Transparency Section (Essential for Viva / College Internal Evaluation)
    with st.expander("🔬 How NLP Analyzed Your Resume (Viva & Academic Inspection)", expanded=False):
        st.markdown(
            "This section demonstrates the internal NLP processing steps performed on the resume, "
            "verifying that classical NLP algorithms are actively functioning."
        )

        v_tab1, v_tab2, v_tab3, v_tab4, v_tab5 = st.tabs([
            "1. Text Cleaning",
            "2. Tokenization",
            "3. Stopwords & Lemmas",
            "4. spaCy NER",
            "5. Summary Metrics"
        ])

        with v_tab1:
            st.markdown("**Raw Extracted Text Sample:**")
            st.text_area("Raw Text", trace["raw_text"], height=120, disabled=True)
            st.markdown("**Cleaned & Normalized Text Sample:**")
            st.text_area("Cleaned Text", trace["cleaned_text"], height=120, disabled=True)

        with v_tab2:
            st.markdown(f"**Total Tokens:** `{trace['total_tokens_count']}`")
            st.markdown("**Sample First 40 Word Tokens:**")
            st.code(json.dumps(trace["sample_tokens"], indent=2), language="json")

        with v_tab3:
            st.markdown(f"**Tokens after Stopword Removal:** `{trace['stopwords_removed_count']}`")
            st.markdown("**Sample Filtered Tokens:**")
            st.write(trace["sample_stopwords_removed"])
            st.markdown("**Sample Lemmatized Root Tokens (WordNet/spaCy):**")
            st.write(trace["sample_lemmas"])

        with v_tab4:
            st.markdown("**spaCy Named Entities Detected:**")
            st.json(trace["named_entities"])

        with v_tab5:
            st.markdown(f"- **Raw Document Characters:** {trace['raw_char_count']}")
            st.markdown(f"- **Total Vocabulary Tokens:** {trace['total_tokens_count']}")
            st.markdown(f"- **Stopwords Removed:** {trace['total_tokens_count'] - trace['stopwords_removed_count']}")
            st.markdown(f"- **Detected Skills:** {trace['extracted_skills_count']}")
            st.markdown(f"- **Detected Sections:** {', '.join(trace['sections_detected'])}")

    st.write("")
    st.info("👉 Next Step: Go to **Find Jobs** in the navigation bar to search current openings or test with a custom job description.")
