# pages/01_home.py — Window 1: Home Page
# Professional white Apple-style design. No emojis. No dark theme.

import streamlit as st

st.set_page_config(
    page_title="SkillDrift — Are You Ready?",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    [data-testid="stSidebarNav"] { display: none; }
    .stApp { background-color: #F5F5F7; }
    .block-container { padding-top: 3rem; padding-bottom: 3rem; }

    .stButton > button {
        border-radius: 8px;
        border: 1px solid #D2D2D7;
        background: #F5F5F7;
        color: #1D1D1F;
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.15s ease;
    }
    .stButton > button:hover { background: #E8E8ED; }
    .stButton > button[kind="primary"] {
        background: #6C63FF;
        color: #FFFFFF;
        border-color: #6C63FF;
        font-size: 1rem;
        padding: 0.6rem 2rem;
    }
    .stButton > button[kind="primary"]:hover { background: #5A52E0; }

    .stat-card {
        background: #FFFFFF;
        border: 1px solid #D2D2D7;
        border-radius: 18px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        height: 100%;
    }
    .stat-number {
        font-size: 3.5rem;
        font-weight: 700;
        color: #FF3B30;
        line-height: 1;
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
    }
    .stat-label {
        font-size: 1rem;
        color: #1D1D1F;
        margin-top: 0.75rem;
        line-height: 1.5;
    }
    .stat-source {
        font-size: 0.75rem;
        color: #86868B;
        margin-top: 0.75rem;
        font-style: italic;
    }
    .section-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #1D1D1F;
        text-align: center;
        margin: 2.5rem 0 1.5rem 0;
    }
    .step-card {
        background: #FFFFFF;
        border: 1px solid #D2D2D7;
        border-radius: 14px;
        padding: 1.5rem;
        text-align: center;
        height: 160px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .step-number {
        font-size: 1.1rem;
        font-weight: 700;
        color: #6C63FF;
        margin-bottom: 0.5rem;
    }
    .step-title {
        font-weight: 700;
        color: #1D1D1F;
        margin-bottom: 0.35rem;
        font-size: 0.95rem;
    }
    .step-desc {
        font-size: 0.85rem;
        color: #86868B;
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)

# ── Top right Faculty Login ──────────────────────────────────
col_spacer, col_faculty_btn = st.columns([8, 2])
with col_faculty_btn:
    if st.button("Faculty / HOD Login", key="faculty_btn"):
        st.switch_page("pages/09_faculty.py")

# ── Hero Section ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 2rem 0 1.5rem 0;">
    <div style="font-size:3.2rem; font-weight:700; color:#1D1D1F; line-height:1.15;
                font-family:-apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;">
        Are You Drifting Toward Unemployment?
    </div>
    <div style="font-size:1.2rem; color:#86868B; margin-top:1rem; max-width:640px;
                margin-left:auto; margin-right:auto; line-height:1.6;">
        SkillDrift analyzes your B.Tech CSE skill pattern and tells you — mathematically —
        whether you are on track for placement or heading toward a gap year.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Three Statistics Cards ────────────────────────────────────
st.markdown('<div class="section-title">The Numbers India Does Not Talk About</div>',
            unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">57%</div>
        <div class="stat-label">
            of Indian CSE graduates are <strong>not hireable</strong>
            at the time of graduation
        </div>
        <div class="stat-source">
            India Skills Report 2024 — Wheebox &amp; Mercer Mettl Graduate Skill Index
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">1M+</div>
        <div class="stat-label">
            tech job vacancies remain <strong>unfilled</strong> because
            candidates lack sufficient depth in any specific skill domain
        </div>
        <div class="stat-source">
            NASSCOM Annual IT Industry Report 2024
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number" style="font-size:2.4rem;">75% vs 35%</div>
        <div class="stat-label">
            Placement rate of <strong>focused students</strong> (one track
            from Semester 3) versus <strong>drifting students</strong>
            (multiple tracks, no depth)
        </div>
        <div class="stat-source">
            AICTE Graduate Outcome Data 2023–24 &amp; NASSCOM Skill-Depth Research
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── What is Skill Drift ───────────────────────────────────────
st.markdown('<div class="section-title">What is Skill Drift?</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2, gap="large")

with col_a:
    st.markdown("""
    <div style="background:#FFFFFF; border:1px solid #D2D2D7; border-radius:14px;
                padding:1.75rem; line-height:1.7; color:#1D1D1F;">
        <strong style="font-size:1rem;">Skill Drift</strong> is what happens when a B.Tech CSE student
        keeps switching technologies every semester without ever going deep enough in any one of them.
        <br><br>
        Semester 1 — Python basics from YouTube<br>
        Semester 2 — Switched to web development<br>
        Semester 3 — Machine Learning is trending<br>
        Semester 5 — Everyone is talking about cloud<br>
        <strong>Semester 8 — Touched 8 fields. Not ready for any.</strong>
        <br><br>
        <span style="color:#86868B;">
        Learning a new technology always feels like progress.
        That feeling is exactly why drift is dangerous.
        </span>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
    <div style="background:#FFFFFF; border:1px solid #D2D2D7; border-radius:14px;
                padding:1.75rem; line-height:1.7; color:#1D1D1F;">
        <strong style="font-size:1rem;">SkillDrift solves this in three ways:</strong>
        <br><br>
        <div style="margin-bottom:1rem;">
            <span style="color:#6C63FF; font-weight:700;">Measures your scatter pattern</span>
            as a number you cannot argue with — the Drift Score and Shannon Entropy Score.
        </div>
        <div style="margin-bottom:1rem;">
            <span style="color:#6C63FF; font-weight:700;">Verifies your actual skill levels</span>
            through a Gemini-powered quiz before any calculation runs — so the analysis is honest.
        </div>
        <div>
            <span style="color:#6C63FF; font-weight:700;">Shows real consequences</span>
            using data from 794 actual Indian job postings collected from Naukri.com
            across 8 CSE career tracks.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── How It Works ──────────────────────────────────────────────
st.markdown('<div class="section-title">How SkillDrift Works</div>', unsafe_allow_html=True)

steps_cols = st.columns(4, gap="medium")
step_data = [
    ("Step 1", "Enter Your Skills",
     "Select your skills across 6 categories and rate your level honestly"),
    ("Step 2", "Take the Verification Quiz",
     "Gemini AI asks questions per skill to verify what you actually know"),
    ("Step 3", "See Your Dashboard",
     "8 analysis windows show your Drift Score, career match, and action plan"),
    ("Step 4", "Download Your Report",
     "Get a CSV report to share with your placement cell or faculty"),
]

for col, (number, title, desc) in zip(steps_cols, step_data):
    with col:
        st.markdown(f"""
        <div class="step-card">
            <div class="step-number">{number}</div>
            <div class="step-title">{title}</div>
            <div class="step-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ── CTA Button ────────────────────────────────────────────────
col_left, col_cta, col_right = st.columns([2, 3, 2])
with col_cta:
    if st.button("Analyze My Career Focus", type="primary", use_container_width=True):
        st.switch_page("pages/02_skill_input.py")

st.markdown("<br>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown("""
<hr style="border: none; border-top: 1px solid #D2D2D7; margin: 2rem 0;">
<div style="text-align:center; color:#86868B; font-size:0.8rem;">
    SkillDrift — Built for B.Tech CSE students in India &nbsp;|&nbsp;
    Data from Naukri.com, India Skills Report 2024, NASSCOM, AICTE &nbsp;|&nbsp;
    Powered by Google Gemini AI
</div>
""", unsafe_allow_html=True)
