# pages/03_drift_score.py — Window 3: Drift Score Dashboard
# BUG FIXED: track_df was built with { ... } (Ellipsis set literal) instead of a real dict.
# This caused KeyError: 'Skills You Have' on sort_values().

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from brain import CAREER_TRACKS
from _sidebar import APPLE_CSS, render_sidebar

st.set_page_config(
    page_title="SkillDrift — Drift Score",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(APPLE_CSS, unsafe_allow_html=True)

if not st.session_state.get("student_name"):
    st.warning("Session not found. Please start from the beginning.")
    st.switch_page("pages/02_skill_input.py")

render_sidebar()

# =============================================================
# MAIN CONTENT
# =============================================================

st.title("Drift Score & Entropy Score")
st.markdown(
    "These two scores are calculated from your **verified** skill profile only. "
    "Skills you failed the quiz for are excluded from all analysis."
)
st.markdown("---")

verified_skills = st.session_state.get("verified_skills", {})

if not verified_skills:
    st.warning(
        "No verified skills found. "
        "This usually means all skills were marked Not Verified in the quiz. "
        "Please go back and re-enter your skills honestly."
    )
    st.stop()

# Safe retrieval — always default to 0 to prevent None arithmetic errors
drift_score   = st.session_state.get("drift_score")   or 0
drift_label   = st.session_state.get("drift_label")   or ""
entropy_score = st.session_state.get("entropy_score") or 0
entropy_label = st.session_state.get("entropy_label") or ""
track_counts  = st.session_state.get("track_counts")  or {}

# ── Score Cards ───────────────────────────────────────────────
col1, col2, col3 = st.columns(3, gap="medium")

drift_color = (
    "#34C759" if drift_score <= 20
    else "#FF9500" if drift_score <= 60
    else "#FF3B30"
)

entropy_color = (
    "#34C759" if entropy_score < 1.2
    else "#FF9500" if entropy_score < 2.0
    else "#FF3B30"
)

with col1:
    st.markdown(f"""
    <div style="background:#FFFFFF; border:2px solid {drift_color};
                border-radius:18px; padding:2rem; text-align:center;
                box-shadow:0 2px 12px rgba(0,0,0,0.06);">
        <div style="color:#86868B; font-size:0.75rem; font-weight:600;
                    letter-spacing:1px; text-transform:uppercase; margin-bottom:0.5rem;">
            Drift Score
        </div>
        <div style="font-size:4rem; font-weight:700; color:{drift_color}; line-height:1;">
            {drift_score}
        </div>
        <div style="color:#1D1D1F; font-size:1rem; font-weight:600; margin-top:0.4rem;">
            {drift_label}
        </div>
        <div style="color:#86868B; font-size:0.8rem; margin-top:0.4rem;">
            0 = Focused &nbsp;|&nbsp; 100 = Scattered
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background:#FFFFFF; border:2px solid {entropy_color};
                border-radius:18px; padding:2rem; text-align:center;
                box-shadow:0 2px 12px rgba(0,0,0,0.06);">
        <div style="color:#86868B; font-size:0.75rem; font-weight:600;
                    letter-spacing:1px; text-transform:uppercase; margin-bottom:0.5rem;">
            Entropy Score
        </div>
        <div style="font-size:4rem; font-weight:700; color:{entropy_color}; line-height:1;">
            {entropy_score}
        </div>
        <div style="color:#1D1D1F; font-size:1rem; font-weight:600; margin-top:0.4rem;">
            {entropy_label}
        </div>
        <div style="color:#86868B; font-size:0.8rem; margin-top:0.4rem;">
            0 bits = Focused &nbsp;|&nbsp; 3 bits = Max Scatter
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    skill_count = len(verified_skills)
    st.markdown(f"""
    <div style="background:#FFFFFF; border:2px solid #6C63FF;
                border-radius:18px; padding:2rem; text-align:center;
                box-shadow:0 2px 12px rgba(0,0,0,0.06);">
        <div style="color:#86868B; font-size:0.75rem; font-weight:600;
                    letter-spacing:1px; text-transform:uppercase; margin-bottom:0.5rem;">
            Verified Skills
        </div>
        <div style="font-size:4rem; font-weight:700; color:#6C63FF; line-height:1;">
            {skill_count}
        </div>
        <div style="color:#1D1D1F; font-size:1rem; font-weight:600; margin-top:0.4rem;">
            Skills Confirmed
        </div>
        <div style="color:#86868B; font-size:0.8rem; margin-top:0.4rem;">
            after Gemini verification
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Interpretation ────────────────────────────────────────────
st.subheader("What These Numbers Mean For You")

col_a, col_b = st.columns(2, gap="large")

if drift_score <= 20:
    drift_interpretation = (
        "Your skills are concentrated in very few tracks — you are not drifting. "
        "This is the ideal pattern for placement readiness."
    )
elif drift_score <= 40:
    drift_interpretation = (
        "Your skills are mostly concentrated but with some spread into adjacent tracks. "
        "Mild drift — manageable, but watch your focus going forward."
    )
elif drift_score <= 60:
    drift_interpretation = (
        "Your skills are visibly spread across multiple tracks. "
        "You are drifting. This needs correction before placement season."
    )
else:
    drift_interpretation = (
        "Your skills are scattered broadly across many unrelated tracks. "
        "Strong drift — your lack of depth in any single track is a placement risk."
    )

with col_a:
    st.markdown("**Drift Score Explained**")
    st.markdown(f"""
    <div style="background:#FFFFFF; border:1px solid #D2D2D7; border-radius:14px;
                padding:1.5rem; color:#1D1D1F; line-height:1.7;">

    Your Drift Score of <strong>{drift_score}</strong> measures how scattered your
    {skill_count} verified skills are across the 8 CSE career tracks.<br><br>

    <strong>Score 0</strong> — All your skills are in one track: no drift, highly focused.<br>
    <strong>Score 100</strong> — Skills equally spread across all 8 tracks: maximum drift.<br><br>

    A focused student targeting Data Analyst typically scores <strong>below 30</strong>.
    Placement-ready profiles from Indian industry data average <strong>Drift Score &le; 25</strong>.<br><br>

    <span style="background:#F5F5F7; border-radius:8px; padding:0.5rem 0.75rem;
                 display:block; border-left:3px solid #6C63FF;">
        <em>{drift_interpretation}</em>
    </span><br>

    <span style="color:#86868B; font-size:0.8rem;">
        Formula: Drift Score = 100 − (normalized standard deviation of skill counts
        across 8 tracks). Reference: Garg &amp; Singh 2022, IJSTEM Vol 9.
    </span>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("**Entropy Score Explained**")
    st.markdown(f"""
    <div style="background:#FFFFFF; border:1px solid #D2D2D7; border-radius:14px;
                padding:1.5rem; color:#1D1D1F; line-height:1.7;">

    Your Entropy Score of <strong>{entropy_score} bits</strong> uses Shannon's Information
    Entropy: H = &minus;&Sigma; p &times; log&#8322;(p), where p is the proportion of your verified
    skills in each career track.<br><br>

    <strong>0 bits</strong> — All skills in one track: perfect order, zero uncertainty.<br>
    <strong>~3 bits</strong> — Skills equally spread across all 8 tracks: maximum disorder.<br><br>

    A focused Data Analyst profile typically scores <strong>below 1.2 bits</strong>.
    Your {entropy_score} bits puts you in the <strong>{entropy_label}</strong> category.<br><br>

    <span style="background:#F5F5F7; border-radius:8px; padding:0.5rem 0.75rem;
                 display:block; border-left:3px solid #6C63FF;">
        <strong>How Drift Score and Entropy differ:</strong><br>
        Drift Score (std-dev based) responds more to the magnitude of the dominant track.
        Entropy is more sensitive to how many tracks you have spread into.
        Both together give a complete picture — they are complementary, not redundant.
    </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Track Breakdown Table ─────────────────────────────────────
# BUG FIX: Was `pd.DataFrame([{ ... } for ...])` where `{ ... }` is a Python
# set containing Ellipsis — not a dict. This caused KeyError: 'Skills You Have'.
# Replaced with a proper dict comprehension.

st.subheader("Skill Distribution Across All 8 Tracks")
st.markdown(
    "More skills concentrated in ONE track = less drift = better placement readiness."
)

total_skill_count = max(len(verified_skills), 1)

if track_counts:
    track_df = pd.DataFrame([
        {
            "Career Track":      track,
            "Skills You Have":   count,
            "Share of Profile":  f"{round(count / total_skill_count * 100, 1)}%",
            "Focus Signal":      (
                "Primary Track"   if count == max(track_counts.values()) and count > 0
                else "Secondary"  if count > 0
                else "None"
            ),
        }
        for track, count in track_counts.items()
    ])

    if not track_df.empty:
        track_df = track_df.sort_values("Skills You Have", ascending=False).reset_index(drop=True)

    # Color Focus Signal column
    def color_focus(val):
        if val == "Primary Track":
            return "color: #6C63FF; font-weight: 700"
        elif val == "Secondary":
            return "color: #FF9500"
        return "color: #86868B"

    styled = track_df.style.map(color_focus, subset=["Focus Signal"])
    st.dataframe(styled, use_container_width=True, hide_index=True)
else:
    st.info("No track data available. Please complete the quiz first.")

st.markdown("---")

# ── Navigation ────────────────────────────────────────────────
col_nav1, col_nav2 = st.columns(2)
with col_nav2:
    if st.button("Next — Urgency Engine", type="primary", use_container_width=True):
        st.switch_page("pages/04_urgency.py")
