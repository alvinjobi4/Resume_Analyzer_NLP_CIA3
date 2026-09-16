import streamlit as st
try:
    from services.job_api import search_jobs, get_mock_jobs
except (ImportError, ValueError):
    from ..services.job_api import search_jobs, get_mock_jobs

def render_jobs_page():
    st.markdown('<h1 class="main-title">Job Search & Selection</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Search for live job openings using RapidAPI JSearch, or paste a custom job description. '
        '<b>Select exactly one job</b> to trigger the NLP matching engine.</p>',
        unsafe_allow_html=True
    )

    # Verify if resume is present
    resume_data = st.session_state.get("resume_data")
    if not resume_data:
        st.warning("⚠️ **No resume uploaded yet.** Please upload your resume in the **Resume Analysis** tab before analyzing matches.")

    tab_api, tab_manual = st.tabs(["🔍 Search Jobs (RapidAPI JSearch)", "📝 Paste Custom Job Description (Offline Fallback)"])

    with tab_api:
        col_q, col_loc, col_ctry = st.columns([2, 1.5, 1])
        with col_q:
            query = st.text_input("Job Title / Keywords", value="Machine Learning Engineer", placeholder="e.g. Python Developer, Data Scientist")
        with col_loc:
            location = st.text_input("Location", value="Bengaluru", placeholder="e.g. Bengaluru, Remote, Chicago")
        with col_ctry:
            country = st.selectbox("Country Code", options=["in", "us", "gb", "ca", "de"], index=0, help="Country code for JSearch API filtering.")

        btn_col1, btn_col2 = st.columns([1, 1])
        with btn_col1:
            search_clicked = st.button("🔎 Search Jobs", type="primary", use_container_width=True)
        with btn_col2:
            mock_clicked = st.button("📦 Load Offline Demo Jobs", use_container_width=True, help="Load pre-configured real-world job postings without consuming API requests.")

        if search_clicked:
            if not query.strip():
                st.error("Please enter a job title or keyword.")
            else:
                with st.spinner(f"Querying RapidAPI JSearch for '{query}' in '{location}' (aggregating live web listings, may take 15-30s)..."):
                    result = search_jobs(query=query, location=location, country=country, num_pages=1)
                    if result["success"]:
                        st.session_state["job_search_results"] = result["jobs"]
                        st.session_state["last_query"] = result["query"]
                        if result["jobs"]:
                            st.success(f"✓ Found {len(result['jobs'])} jobs returned by JSearch.")
                        else:
                            st.warning("No jobs returned for this search query. Try another keyword or location.")
                    else:
                        st.error(f"API Error: {result['error']}")
                        st.info("💡 RapidAPI job aggregation can experience latency during peak hours. You can also click **'Load Offline Demo Jobs'** above or paste any job into the **'Paste Custom Job Description'** tab.")

        if mock_clicked:
            mock_jobs = get_mock_jobs()
            st.session_state["job_search_results"] = mock_jobs
            st.session_state["last_query"] = "Demo Sample Jobs"
            st.success(f"✓ Loaded {len(mock_jobs)} offline curated demo jobs.")

        # Display Jobs
        jobs_list = st.session_state.get("job_search_results", [])
        if jobs_list:
            st.markdown(f"### Results for: *{st.session_state.get('last_query', query)}*")
            st.caption("Note: NLP matching will only be executed on the **specific job** you select by clicking 'Analyze Match'.")

            for idx, job in enumerate(jobs_list):
                with st.container():
                    st.markdown(
                        f"""
                        <div class="job-card">
                            <h3 style="margin-top:0; color:#1e293b;">{job['title']}</h3>
                            <p style="color:#475569; margin-bottom:8px;">
                                🏢 <b>{job['company']}</b> &nbsp;|&nbsp; 📍 {job['location']} &nbsp;|&nbsp; ⏱ {job['job_type']}
                            </p>
                            <p style="color:#64748b; font-size:0.9rem;">
                                💵 Salary: <b>{job['salary']}</b> &nbsp;|&nbsp; 📅 Posted: {job['date_posted']} &nbsp;|&nbsp; 🌐 Source: {job['source']}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    c1, c2, c3 = st.columns([1.5, 1, 2.5])
                    with c1:
                        if st.button(f"⚡ Analyze Match", key=f"btn_analyze_{job['job_id']}_{idx}", type="primary", use_container_width=True):
                            st.session_state["selected_job"] = job
                            st.session_state["current_page"] = "Job Match Analysis"
                            st.rerun()
                    with c2:
                        if job["apply_url"] and job["apply_url"] != "#":
                            st.link_button("↗ Apply / View", job["apply_url"], use_container_width=True)
                    with c3:
                        with st.expander("View Full Job Description", expanded=False):
                            st.write(job["description"])

                    st.write("")

    with tab_manual:
        st.markdown("### Paste a Specific Job Description")
        st.markdown("If you wish to test a specific job posting from any company, enter it below:")

        man_title = st.text_input("Job Title", value="Senior Machine Learning Engineer")
        man_company = st.text_input("Company Name", value="Enterprise AI Corp")
        man_location = st.text_input("Job Location", value="Bengaluru, India / Remote")
        man_desc = st.text_area(
            "Job Description & Requirements",
            height=200,
            value=(
                "We are hiring a Senior Machine Learning Engineer.\n\n"
                "Requirements:\n"
                "- Strong proficiency in Python, Machine Learning, and NLP.\n"
                "- Experience with TensorFlow, PyTorch, Scikit-learn, and Pandas.\n"
                "- Solid background in SQL, PostgreSQL, Docker, and AWS.\n"
                "- Bachelor's or Master's degree in Computer Science.\n"
                "- 3+ years of practical software development experience."
            )
        )

        if st.button("⚡ Analyze This Custom Job", type="primary"):
            custom_job = {
                "job_id": "custom-pasted-job",
                "title": man_title,
                "company": man_company,
                "location": man_location,
                "description": man_desc,
                "job_type": "Full-time",
                "salary": "Not provided",
                "date_posted": "Custom Input",
                "apply_url": "#",
                "source": "Custom Text Input"
            }
            st.session_state["selected_job"] = custom_job
            st.session_state["current_page"] = "Job Match Analysis"
            st.rerun()
