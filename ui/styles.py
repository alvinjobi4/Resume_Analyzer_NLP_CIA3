CUSTOM_CSS = """
<style>
/* Global Modern Styling */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Header & Banner */
.main-title {
    background: linear-gradient(135deg, #2563eb 0%, #7c3aed 50%, #db2777 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    font-size: 2.3rem;
    margin-bottom: 0.2rem;
    letter-spacing: -0.02em;
}

.subtitle {
    color: #64748b;
    font-size: 1.05rem;
    font-weight: 400;
    margin-bottom: 1.5rem;
}

/* Glassmorphic Metric Cards */
.metric-card {
    background: linear-gradient(145deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
    border: 1px solid rgba(226, 232, 240, 0.2);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
    backdrop-filter: blur(10px);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 30px -5px rgba(0, 0, 0, 0.08);
}

/* Job Result Cards */
.job-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 18px;
    transition: all 0.2s ease-in-out;
}

.job-card:hover {
    border-color: #3b82f6;
    box-shadow: 0 12px 24px -6px rgba(59, 130, 246, 0.12);
}

/* Skill Badges */
.skill-badge {
    display: inline-block;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 3px 4px;
    letter-spacing: 0.01em;
}

.skill-match {
    background-color: #ecfdf5;
    color: #065f46;
    border: 1px solid #a7f3d0;
}

.skill-missing {
    background-color: #fef2f2;
    color: #991b1b;
    border: 1px solid #fecaca;
}

.skill-neutral {
    background-color: #f1f5f9;
    color: #334155;
    border: 1px solid #cbd5e1;
}

/* Score Circle / Badge */
.score-badge {
    font-size: 2.8rem;
    font-weight: 800;
    line-height: 1;
    margin: 10px 0;
}

.score-label {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 30px;
    font-size: 0.95rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Viva Section Callout */
.viva-callout {
    background: #f8fafc;
    border-left: 4px solid #3b82f6;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin: 12px 0;
    font-size: 0.92rem;
}

/* Buttons */
div.stButton > button:first-child {
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.2s ease;
}
</style>
"""
