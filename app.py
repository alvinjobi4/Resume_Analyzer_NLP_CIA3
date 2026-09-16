import streamlit as st
import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config.settings import RAPIDAPI_KEY
from ui.styles import CUSTOM_CSS
from ui.resume_page import render_resume_page
from ui.jobs_page import render_jobs_page
from ui.analysis_page import render_analysis_page

def init_session_state():
    """Initializes Streamlit session state variables."""
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Home"
    if "resume_data" not in st.session_state:
        st.session_state["resume_data"] = None
    if "resume_filename" not in st.session_state:
        st.session_state["resume_filename"] = None
    if "selected_job" not in st.session_state:
        st.session_state["selected_job"] = None
    if "job_search_results" not in st.session_state:
        st.session_state["job_search_results"] = []

def render_home_page():
    st.markdown('<h1 class="main-title">NLP-Based Intelligent Resume Analysis & Job Matching System</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">An academic NLP system leveraging Document Parsing, spaCy NER, Lemmatization, '
        'TF-IDF Vectorization, and Cosine Similarity to compute genuine candidate-job fit analytics.</p>',
        unsafe_allow_html=True
    )

    # Workflow cards
    st.markdown("### 🔄 Exact System Workflow")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
            <div class="metric-card" style="height:170px;">
                <h4>1. Resume NLP</h4>
                <p style="font-size:0.85rem; color:#475569;">
                    Upload PDF or DOCX. Automated text cleaning, lemmatization, spaCy NER, section detection, and skill extraction.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="metric-card" style="height:170px;">
                <h4>2. Job Discovery</h4>
                <p style="font-size:0.85rem; color:#475569;">
                    Query live job postings using RapidAPI JSearch. Display structured job cards with titles, employers, and compensation.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="metric-card" style="height:170px;">
                <h4>3. Selective NLP</h4>
                <p style="font-size:0.85rem; color:#475569;">
                    Select <b>ONE</b> job of interest. The system parses only that specific job description through the NLP pipeline.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            """
            <div class="metric-card" style="height:170px;">
                <h4>4. Match Analytics</h4>
                <p style="font-size:0.85rem; color:#475569;">
                    Calculate TF-IDF Cosine Similarity, skill overlap & gaps, requirement checks, and actionable resume recommendations.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")
    start_btn = st.button("🚀 Upload Resume to Begin", type="primary", use_container_width=True)
    if start_btn:
        st.session_state["current_page"] = "Upload Resume"
        st.rerun()

    st.divider()

    # Core Academic NLP Architecture
    st.markdown("### 🧠 Core NLP Algorithms & Techniques")
    a_col1, a_col2 = st.columns(2)

    with a_col1:
        st.markdown(
            """
            - **Text Cleaning & Token-Safe Punctuation**: Preserves programming tokens (`C++`, `C#`, `.NET`, `Node.js`) while stripping non-printable noise and symbols.
            - **Tokenization & Lemmatization**: Word tokenization combined with NLTK / spaCy WordNet lemmatizers (`developing` $\\to$ `develop`, `models` $\\to$ `model`).
            - **Named Entity Recognition (NER)**: spaCy `en_core_web_sm` identifies `PERSON`, `ORG`, `GPE` (locations), and `DATE` entities to discover candidates and employers.
            - **Section Detection**: Layout-aware heuristic regex categorizing text into `EDUCATION`, `SKILLS`, `EXPERIENCE`, and `PROJECTS`.
            """
        )

    with a_col2:
        st.markdown(
            """
            - **Taxonomy-Based Skill Extraction**: Dynamic dictionary of technical skills supporting alias normalization (`ML` $\\to$ `Machine Learning`, `sklearn` $\\to$ `Scikit-learn`).
            - **TF-IDF Vector Space**: `TfidfVectorizer` computes n-gram (1, 2) feature vectors over the preprocessed resume and job description.
            - **Cosine Similarity Calculation**: Evaluates the directional cosine angle between the two document vectors.
            - **Weighted Mathematical Scoring**:
              $$\\text{Score} = (0.50 \\times \\text{TF-IDF}) + (0.40 \\times \\text{Skill Match}) + (0.10 \\times \\text{Requirements})$$
            """
        )

def main():
    st.set_page_config(
        page_title="NLP Resume & Job Matcher",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Inject modern custom CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # Initialize state
    init_session_state()

    # Sidebar
    with st.sidebar:
        st.markdown("## 🎯 NLP Resume Matcher")
        st.caption("College NLP Course Project & Evaluation")
        st.divider()

        # Session Status
        st.markdown("### 📌 Status Overview")
        if st.session_state.get("resume_data"):
            cand_name = st.session_state["resume_data"]["candidate_profile"]["name"]
            st.success(f"✓ Resume: **{cand_name}**")
        else:
            st.info("○ No resume loaded")

        if st.session_state.get("selected_job"):
            job_title = st.session_state["selected_job"]["title"]
            st.success(f"✓ Target Job: **{job_title[:22]}...**")
        else:
            st.info("○ No job selected")

        st.divider()

        # Navigation
        st.markdown("### 🧭 Navigation")
        pages = ["Home", "Upload Resume", "Find Jobs", "Job Match Analysis"]
        
        # Determine current index
        try:
            current_idx = pages.index(st.session_state.get("current_page", "Home"))
        except ValueError:
            current_idx = 0

        nav_choice = st.radio(
            "Go to Page:",
            pages,
            index=current_idx,
            label_visibility="collapsed"
        )

        if nav_choice != st.session_state["current_page"]:
            st.session_state["current_page"] = nav_choice
            st.rerun()

        st.divider()

        # Reset button
        if st.button("🔄 Reset Application State", use_container_width=True):
            st.session_state["resume_data"] = None
            st.session_state["resume_filename"] = None
            st.session_state["selected_job"] = None
            st.session_state["job_search_results"] = []
            st.session_state["current_page"] = "Home"
            st.rerun()

        with st.expander("ℹ️ RapidAPI Config", expanded=False):
            if RAPIDAPI_KEY and RAPIDAPI_KEY != "your_rapidapi_key_here":
                masked_key = RAPIDAPI_KEY[:4] + "..." + RAPIDAPI_KEY[-4:]
                st.write(f"Key: `{masked_key}`")
                st.caption("Status: Configured via .env")
            else:
                st.warning("RapidAPI key missing in .env")

    # Routing
    current_page = st.session_state.get("current_page", "Home")
    if current_page == "Home":
        render_home_page()
    elif current_page == "Upload Resume":
        render_resume_page()
    elif current_page == "Find Jobs":
        render_jobs_page()
    elif current_page == "Job Match Analysis":
        render_analysis_page()

if __name__ == "__main__":
    main()
