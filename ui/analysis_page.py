import streamlit as st
import plotly.graph_objects as go
import json

try:
    from nlp.job_analyzer import analyze_job_description
    from nlp.similarity import calculate_tfidf_cosine_similarity
    from scoring.match_score import compute_overall_match
    from scoring.recommendations import generate_recommendations
except (ImportError, ValueError):
    from ..nlp.job_analyzer import analyze_job_description
    from ..nlp.similarity import calculate_tfidf_cosine_similarity
    from ..scoring.match_score import compute_overall_match
    from ..scoring.recommendations import generate_recommendations

def render_analysis_page():
    st.markdown('<h1 class="main-title">Job Match Analysis</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Detailed NLP-powered comparison between your uploaded resume profile and the selected job description.</p>',
        unsafe_allow_html=True
    )

    resume_data = st.session_state.get("resume_data")
    selected_job = st.session_state.get("selected_job")

    if not resume_data:
        st.warning("⚠️ **No resume uploaded.** Please upload a resume in the **Upload Resume** tab first.")
        return

    if not selected_job:
        st.info("ℹ️ **No job selected for analysis.** Please choose a job from **Find Jobs** and click **'Analyze Match'**.")
        return

    # Process ONLY the selected job through the NLP pipeline
    with st.spinner("Analyzing selected job description and computing NLP match score..."):
        job_nlp = analyze_job_description(selected_job.get("description", ""))
        
        # Calculate TF-IDF & Cosine Similarity
        similarity_data = calculate_tfidf_cosine_similarity(
            text1=resume_data["cleaned_text"],
            text2=job_nlp["cleaned_text"]
        )

        candidate_profile = resume_data["candidate_profile"]

        # Compute Overall Weighted Match
        match_result = compute_overall_match(
            resume_skills=candidate_profile["skills"],
            job_skills=job_nlp["skills"],
            tfidf_similarity_percentage=similarity_data["similarity_percentage"],
            candidate_education=candidate_profile["education"],
            job_education=job_nlp["education_requirement"],
            candidate_years=candidate_profile["experience_years"],
            job_experience=job_nlp["experience_requirement"]
        )

        # Generate targeted recommendations based on missing items
        recommendations = generate_recommendations(match_result, selected_job.get("title", "Position"))

    # Selected Job Summary Card
    st.markdown(
        f"""
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:12px; padding:18px; margin-bottom:20px;">
            <span style="font-size:0.85rem; color:#64748b; font-weight:600; text-transform:uppercase;">Selected Target Job</span>
            <h2 style="margin:4px 0; color:#0f172a;">{selected_job.get('title')}</h2>
            <p style="margin:0; color:#475569;">🏢 <b>{selected_job.get('company')}</b> &nbsp;|&nbsp; 📍 {selected_job.get('location')} &nbsp;|&nbsp; ⏱ {selected_job.get('job_type')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Top Section: Overall Score and Breakdown Chart
    score_col, chart_col = st.columns([1.2, 2])

    with score_col:
        st.markdown(
            f"""
            <div class="metric-card" style="text-align:center; padding:25px 15px;">
                <div style="font-size:0.9rem; font-weight:700; color:#64748b; text-transform:uppercase; letter-spacing:0.05em;">Overall Match Score</div>
                <div class="score-badge" style="color:{match_result['category_color']};">
                    {match_result['overall_score']}%
                </div>
                <div class="score-label" style="background:{match_result['category_color']}15; color:{match_result['category_color']}; border:1px solid {match_result['category_color']}40;">
                    {match_result['category']}
                </div>
                <div style="margin-top:15px; font-size:0.85rem; color:#64748b;">
                    Candidate: <b>{candidate_profile['name']}</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with chart_col:
        # Score Breakdown Plotly Horizontal Bar
        breakdown = match_result["score_breakdown"]
        categories = ['TF-IDF Similarity (50%)', 'Skill Match (40%)', 'Requirements (10%)']
        scores = [breakdown['tfidf_similarity'], breakdown['skill_match'], breakdown['requirement_match']]
        colors = ['#3b82f6', '#10b981', '#8b5cf6']

        fig = go.Figure(go.Bar(
            x=scores,
            y=categories,
            orientation='h',
            marker=dict(color=colors, line=dict(width=0)),
            text=[f"{s}%" for s in scores],
            textposition='auto',
        ))
        fig.update_layout(
            title="Dynamic NLP Score Breakdown",
            xaxis=dict(range=[0, 100], title="Percentage (%)"),
            yaxis=dict(autorange="reversed"),
            height=200,
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Skills Analysis: Matching vs Missing Skills
    st.markdown("### 🎯 Skills Compatibility Analysis")
    skills_data = match_result["skills_analysis"]

    sk_col1, sk_col2 = st.columns(2)
    with sk_col1:
        st.markdown(f"#### ✓ Matching Skills ({skills_data['total_matched_skills_count']})")
        if skills_data["matching_skills"]:
            badges_html = " ".join([f'<span class="skill-badge skill-match">✓ {s}</span>' for s in skills_data["matching_skills"]])
            st.markdown(badges_html, unsafe_allow_html=True)
        else:
            st.info("No overlapping technical skills detected from the configured dictionary.")

    with sk_col2:
        st.markdown(f"#### ✗ Missing Skills ({skills_data['total_missing_skills_count']})")
        if skills_data["missing_skills"]:
            badges_html = " ".join([f'<span class="skill-badge skill-missing">✗ {s}</span>' for s in skills_data["missing_skills"]])
            st.markdown(badges_html, unsafe_allow_html=True)
        else:
            st.success("✓ All identified technical requirements from the job description are present in your resume!")

    st.divider()

    # Education and Experience Comparison
    st.markdown("### 📋 Education & Experience Requirements")
    req_col1, req_col2 = st.columns(2)

    with req_col1:
        edu_match = match_result["education_match"]
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>🎓 Education Comparison</h4>
                <p><b>Job Requirement:</b> {job_nlp['education_requirement']['text']}</p>
                <p><b>Resume Education:</b> {', '.join(candidate_profile['education'][:2])}</p>
                <p><b>Status:</b> <span class="skill-badge skill-neutral">{edu_match['badge']}</span></p>
                <p style="font-size:0.88rem; color:#64748b;">{edu_match['message']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with req_col2:
        exp_match = match_result["experience_match"]
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>⏱ Experience Comparison</h4>
                <p><b>Job Requirement:</b> {job_nlp['experience_requirement']['text']}</p>
                <p><b>Resume Experience:</b> ~{candidate_profile['experience_years']} years documented</p>
                <p><b>Status:</b> <span class="skill-badge skill-neutral">{exp_match['badge']}</span></p>
                <p style="font-size:0.88rem; color:#64748b;">{exp_match['message']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # Recommendations Engine (Genuinely derived from gaps)
    st.markdown("### 💡 Targeted Recommendations to Improve Match")
    st.caption("Recommendations are dynamically derived from missing skills, requirement gaps, and TF-IDF keyword coverage.")

    for idx, rec in enumerate(recommendations):
        priority_color = "#ef4444" if rec["priority"] == "High" else "#f59e0b" if rec["priority"] == "Medium" else "#3b82f6"
        st.markdown(
            f"""
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-left:4px solid {priority_color}; border-radius:8px; padding:14px 18px; margin-bottom:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b>{rec['recommendation']}</b>
                    <span style="font-size:0.75rem; background:{priority_color}15; color:{priority_color}; padding:2px 8px; border-radius:12px; font-weight:700;">{rec['priority']} Priority</span>
                </div>
                <div style="font-size:0.88rem; color:#475569; margin-top:6px;">{rec['action']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # Academic NLP Transparency & Viva Deep Dive
    with st.expander("🔬 How NLP Analyzed This Match (Academic Viva & Internal Evaluation)", expanded=False):
        st.markdown(
            "This section presents the mathematical formulas, TF-IDF vectors, and entity extractions "
            "used to produce the score above."
        )

        viva_tab1, viva_tab2, viva_tab3, viva_tab4, viva_tab5 = st.tabs([
            "1. TF-IDF & Cosine Similarity",
            "2. Top Shared Keywords",
            "3. Job NLP Processing",
            "4. Scoring Formula",
            "5. Raw Payload Inspector"
        ])

        with viva_tab1:
            st.markdown("#### Mathematical Formulation")
            st.latex(r"\text{Similarity} = \cos(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\|_2 \|\mathbf{B}\|_2} = \frac{\sum_{i=1}^n A_i B_i}{\sqrt{\sum_{i=1}^n A_i^2} \sqrt{\sum_{i=1}^n B_i^2}}")
            st.markdown(
                f"- **Vector Vocabulary Size:** `{similarity_data['vocabulary_size']}` unique n-grams\n"
                f"- **Cosine Similarity Value:** `{similarity_data['similarity_score']:.4f}`\n"
                f"- **TF-IDF Percentage:** `{similarity_data['similarity_percentage']}%`"
            )

        with viva_tab2:
            st.markdown("#### High-Impact Shared Terms (Terms with High TF-IDF in Both Documents)")
            if similarity_data["common_terms"]:
                terms_table = [
                    {"Term": item["term"], "Resume Weight": item["resume_weight"], "Job Weight": item["job_weight"], "Combined Impact": item["combined_impact"]}
                    for item in similarity_data["common_terms"]
                ]
                st.table(terms_table)
            else:
                st.info("No significant overlapping high-weight terms detected.")

            st.markdown("#### Distinctive Terms")
            dt_col1, dt_col2 = st.columns(2)
            with dt_col1:
                st.markdown("**Top Resume Terms:**")
                st.json(similarity_data["top_resume_terms"])
            with dt_col2:
                st.markdown("**Top Job Terms:**")
                st.json(similarity_data["top_job_terms"])

        with viva_tab3:
            st.markdown("#### Selected Job NLP Tokenization & Extraction")
            st.markdown(f"- **Total Word Tokens:** `{len(job_nlp['tokens'])}`")
            st.markdown(f"- **Stopwords Removed:** `{len(job_nlp['tokens']) - len(job_nlp['stopwords_removed'])}`")
            st.markdown(f"- **Detected Skills:** `{', '.join(job_nlp['skills'])}`")
            st.markdown(f"- **Detected Experience Requirement:** `{job_nlp['experience_requirement']['text']}`")
            st.markdown(f"- **Detected Education Requirement:** `{job_nlp['education_requirement']['text']}`")
            if job_nlp["key_requirements"]:
                st.markdown("**Key Extracted Requirement Sentences:**")
                for req in job_nlp["key_requirements"]:
                    st.markdown(f"- {req}")

        with viva_tab4:
            st.markdown("#### Exact Weighted Score Calculation")
            st.latex(r"\text{Overall Score} = (0.50 \times \text{TF-IDF}) + (0.40 \times \text{Skill}) + (0.10 \times \text{Requirements})")
            st.markdown(
                f"$$\\text{{Overall Score}} = (0.50 \\times {breakdown['tfidf_similarity']}) + "
                f"(0.40 \\times {breakdown['skill_match']}) + "
                f"(0.10 \\times {breakdown['requirement_match']}) = {match_result['overall_score']}\\%$$"
            )

        with viva_tab5:
            st.markdown("#### Full Match Result JSON Payload")
            st.json(match_result)
