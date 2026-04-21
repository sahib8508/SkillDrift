# Window 3 - Drift Score 
# =============================================================
# pages/03_drift_score.py — Window 3: Drift Score Dashboard
# =============================================================

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from brain import CAREER_TRACKS

st.set_page_config(
    page_title="SkillDrift — Your Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

if not st.session_state.get("student_name"):
    st.warning("⚠️ Session not found. Please start from the beginning.")
    st.switch_page("pages/02_skill_input.py")

# =============================================================
# SIDEBAR
# =============================================================

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0;">
        <svg width="80" height="80" viewBox="0 0 80 80"
             xmlns="http://www.w3.org/2000/svg">
            <circle cx="40" cy="40" r="40" fill="#2D3250"/>
            <circle cx="40" cy="30" r="15" fill="#6C63FF"/>
            <ellipse cx="40" cy="65" rx="22" ry="15" fill="#6C63FF"/>
        </svg>
    </div>
    """, unsafe_allow_html=True)

    student_name = st.session_state.get("student_name", "Student")
    st.markdown(
        f"<div style='text-align:center; font-weight:700; "
        f"font-size:1.1rem; color:#FAFAFA;'>{student_name}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div style='text-align:center; color:#7F8C8D; font-size:0.85rem;'>"
        f"Semester {st.session_state.get('semester', '?')}</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    drift_score   = st.session_state.get("drift_score")
    drift_label   = st.session_state.get("drift_label", "")
    entropy_score = st.session_state.get("entropy_score")
    entropy_label = st.session_state.get("entropy_label", "")
    # ✅ SAFETY FIX (MANDATORY)
    if drift_score is None:
        drift_score = 0

    if entropy_score is None:
        entropy_score = 0

    if drift_score is not None:
        # LOW drift = focused = good = GREEN
        # HIGH drift = scattered = bad = RED
        drift_color = (
            "#2ECC71" if drift_score <= 20
            else "#F39C12" if drift_score <= 60
            else "#E74C3C"
        )
        st.markdown(f"""
        <div style="background:#1A1D27; border:1px solid #2D3250;
                    border-radius:8px; padding:1rem; margin-bottom:0.75rem;">
            <div style="color:#7F8C8D; font-size:0.8rem;">DRIFT SCORE</div>
            <div style="font-size:2rem; font-weight:900; color:{drift_color};">
                {drift_score}
            </div>
            <div style="color:#BDC3C7; font-size:0.85rem;">{drift_label}</div>
        </div>
        """, unsafe_allow_html=True)

        # LOW entropy = ordered = focused = GREEN
        # HIGH entropy = disordered = scattered = RED
        entropy_color = (
            "#2ECC71" if entropy_score < 1.2
            else "#F39C12" if entropy_score < 2.0
            else "#E74C3C"
        )
        st.markdown(f"""
        <div style="background:#1A1D27; border:1px solid #2D3250;
                    border-radius:8px; padding:1rem; margin-bottom:0.75rem;">
            <div style="color:#7F8C8D; font-size:0.8rem;">ENTROPY SCORE</div>
            <div style="font-size:2rem; font-weight:900; color:{entropy_color};">
                {entropy_score} <span style="font-size:1rem;">bits</span>
            </div>
            <div style="color:#BDC3C7; font-size:0.85rem;">{entropy_label}</div>
        </div>
        """, unsafe_allow_html=True)

        track_counts = st.session_state.get("track_counts", {})
        if track_counts:
            tracks = list(track_counts.keys())
            counts = list(track_counts.values())
            counts_closed = counts + [counts[0]]
            tracks_closed = tracks + [tracks[0]]

            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=counts_closed,
                theta=tracks_closed,
                fill="toself",
                fillcolor="rgba(108, 99, 255, 0.3)",
                line=dict(color="#6C63FF", width=2),
                name="Your Skills",
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, showticklabels=False, gridcolor="#2D3250"),
                    angularaxis=dict(tickfont=dict(size=9, color="#BDC3C7"), gridcolor="#2D3250"),
                    bgcolor="#0E1117",
                ),
                paper_bgcolor="#0E1117",
                plot_bgcolor="#0E1117",
                showlegend=False,
                margin=dict(l=20, r=20, t=20, b=20),
                height=280,
            )
            st.plotly_chart(fig_radar, width="stretch")
    else:
        st.info("Complete the skill quiz to see your scores here.")

    st.markdown("---")
    st.markdown("**📊 Your Dashboard**")
    nav_pages = [
        ("🎯 Drift & Entropy Scores", "pages/03_drift_score.py"),
        ("⏰ Urgency Engine",          "pages/04_urgency.py"),
        ("🏆 Career Track Match",      "pages/05_career_match.py"),
        ("📚 Next Skill & Readiness",  "pages/06_next_skill.py"),
        ("👥 Peer Mirror",             "pages/07_peer_mirror.py"),
        ("🗺️ Market Intelligence",    "pages/08_market_intel.py"),
        ("📄 Final Report",            "pages/10_final_report.py"),
    ]
    for label, page in nav_pages:
        if st.button(label, width="stretch", key=f"nav_{page}"):
            st.switch_page(page)

    st.markdown("---")
    if st.button("🚪 Log Out", width="stretch"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("pages/01_home.py")

# =============================================================
# MAIN CONTENT
# =============================================================

st.title("🎯 Your Drift Score & Entropy Score")
st.markdown(
    "These two scores are calculated from your **verified** skill profile only. "
    "Skills you failed the quiz for are excluded from all analysis."
)
st.markdown("---")

verified_skills = st.session_state.get("verified_skills", {})

if not verified_skills:
    st.warning(
        "⚠️ No verified skills found. "
        "This usually means all skills were marked Not Verified in the quiz. "
        "Please go back and re-enter your skills honestly."
    )
    st.stop()

drift_score   = st.session_state.get("drift_score")
drift_label   = st.session_state.get("drift_label")
entropy_score = st.session_state.get("entropy_score")
entropy_label = st.session_state.get("entropy_label")
track_counts  = st.session_state.get("track_counts") or {}
# ✅ FINAL SAFETY FIX (MAIN SECTION)
if drift_score is None:
    drift_score = 0

if entropy_score is None:
    entropy_score = 0

# ── Score Display ─────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    # LOW drift = focused = GREEN; HIGH drift = scattered = RED
    drift_color = (
        "#2ECC71" if drift_score <= 20
        else "#F39C12" if drift_score <= 60
        else "#E74C3C"
    )
    st.markdown(f"""
    <div style="background:#1A1D27; border:2px solid {drift_color};
                border-radius:12px; padding:2rem; text-align:center;">
        <div style="color:#7F8C8D; font-size:0.9rem; margin-bottom:0.5rem;">
            DRIFT SCORE
        </div>
        <div style="font-size:4rem; font-weight:900; color:{drift_color};">
            {drift_score}
        </div>
        <div style="color:#FAFAFA; font-size:1.1rem; font-weight:600;">
            {drift_label}
        </div>
        <div style="color:#7F8C8D; font-size:0.8rem; margin-top:0.5rem;">
            0 = Focused &nbsp;|&nbsp; 100 = Scattered
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    entropy_color = (
        "#2ECC71" if entropy_score < 1.2
        else "#F39C12" if entropy_score < 2.0
        else "#E74C3C"
    )
    st.markdown(f"""
    <div style="background:#1A1D27; border:2px solid {entropy_color};
                border-radius:12px; padding:2rem; text-align:center;">
        <div style="color:#7F8C8D; font-size:0.9rem; margin-bottom:0.5rem;">
            ENTROPY SCORE
        </div>
        <div style="font-size:4rem; font-weight:900; color:{entropy_color};">
            {entropy_score}
        </div>
        <div style="color:#FAFAFA; font-size:1.1rem; font-weight:600;">
            {entropy_label}
        </div>
        <div style="color:#7F8C8D; font-size:0.8rem; margin-top:0.5rem;">
            0 bits = Focused &nbsp;|&nbsp; 3 bits = Max Scatter
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    skill_count = len(verified_skills)
    st.markdown(f"""
    <div style="background:#1A1D27; border:2px solid #6C63FF;
                border-radius:12px; padding:2rem; text-align:center;">
        <div style="color:#7F8C8D; font-size:0.9rem; margin-bottom:0.5rem;">
            VERIFIED SKILLS
        </div>
        <div style="font-size:4rem; font-weight:900; color:#6C63FF;">
            {skill_count}
        </div>
        <div style="color:#FAFAFA; font-size:1.1rem; font-weight:600;">
            Skills Confirmed
        </div>
        <div style="color:#7F8C8D; font-size:0.8rem; margin-top:0.5rem;">
            after Gemini verification
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── What Your Scores Mean ─────────────────────────────────────
st.subheader("📖 What These Numbers Mean For You")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("**Drift Score Explained**")

    if drift_score <= 20:
        interpretation = (
            "Your skills are concentrated in very few tracks — you are not drifting. "
            "This is the ideal pattern for placement readiness."
        )
    elif drift_score <= 40:
        interpretation = (
            "Your skills are mostly concentrated but with some spread into adjacent tracks. "
            "Mild drift — manageable but watch your focus going forward."
        )
    elif drift_score <= 60:
        interpretation = (
            "Your skills are visibly spread across multiple tracks. "
            "You are drifting. This needs correction before placement season."
        )
    else:
        interpretation = (
            "Your skills are scattered broadly across many unrelated tracks. "
            "This is strong drift — your lack of depth in any single track is a placement risk."
        )

    st.markdown(f"""
    Your Drift Score of **{drift_score}** measures how scattered your
    {skill_count} verified skills are across the 8 CSE career tracks.

    **Score 0** = All your skills are in one track → no drift → highly focused ✅

    **Score 100** = Skills equally spread across all 8 tracks → maximum drift ❌

    A focused student targeting Data Analyst typically scores **below 30**.
    Placement-ready profiles from Indian industry data average **Drift Score ≤ 25**.

    > **Your interpretation:** {interpretation}

    *Formula: Drift Score = 100 − (normalized standard deviation of skill counts
    across 8 tracks). Based on: Garg & Singh 2022, "Skill Portfolio Concentration
    Metrics for Graduate Employability Prediction", IJSTEM Vol 9.*
    """)

with col_b:
    st.markdown("**Entropy Score Explained**")
    st.markdown(f"""
    Your Entropy Score of **{entropy_score} bits** uses **Shannon's Information
    Entropy**: H = −Σ p × log₂(p), where p is the proportion of your verified
    skills in each career track.

    **0 bits** = All skills in one track → perfect order → zero uncertainty ✅

    **~3 bits** = Skills equally spread across all 8 tracks → maximum disorder ❌

    A focused Data Analyst profile typically scores **below 1.2 bits**.
    Your {entropy_score} bits puts you in the **{entropy_label}** category.

    **How Drift Score and Entropy differ:**
    Both measure skill scatter, but through different mathematical lenses.
    Drift Score (std-dev based) is more sensitive to the *magnitude* of the
    dominant track. Entropy is more sensitive to *how many tracks* you have
    spread into. A student with 15 skills in Data Analyst and 1 each in
    5 other tracks gets a good Drift Score but slightly elevated Entropy.
    Both together give a complete picture.
    """)

st.markdown("---")

# ── Track Breakdown Table ─────────────────────────────────────
st.subheader("📊 Your Skill Distribution Across All 8 Tracks")
st.markdown(
    "More skills concentrated in ONE track = less drift = better placement readiness."
)

track_df = pd.DataFrame([
    { ... }
    for track, count in track_counts.items()
])
if not track_df.empty:
    track_df = track_df.sort_values("Skills You Have", ascending=False)

st.dataframe(track_df, width="stretch", hide_index=True)

st.markdown("---")

# ── Navigation ────────────────────────────────────────────────
col_nav1, col_nav2 = st.columns(2)
with col_nav2:
    if st.button("Next → Urgency Engine ⏰", type="primary", width="stretch"):
        st.switch_page("pages/04_urgency.py")
