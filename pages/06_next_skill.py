# pages/06_next_skill.py — Window 6: Next Skill & Readiness Score

import streamlit as st
import plotly.graph_objects as go
from _sidebar import APPLE_CSS, render_sidebar

st.set_page_config(
    page_title="SkillDrift — Next Skill",
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

st.title("Next Skill & Readiness Score")
st.markdown(
    "One action. One reason. One priority. "
    "This page cuts through paralysis and tells you exactly what to study next."
)
st.markdown("---")

next_skill_info = st.session_state.get("next_skill_info", {})
readiness_score = st.session_state.get("readiness_score", 0.0) or 0.0
best_track      = st.session_state.get("best_track", "your best matching track")
career_matches  = st.session_state.get("career_matches", [])

if not next_skill_info and not career_matches:
    st.warning("Data not found. Please complete the quiz first.")
    st.stop()

# ── Next Skill Action Card ────────────────────────────────────
if next_skill_info:
    next_skill_name = next_skill_info.get("skill", "Unknown")
    next_skill_freq = next_skill_info.get("frequency_pct", 0.0)
    next_skill_why  = next_skill_info.get("reason", "")

    st.markdown(f"""
    <div style="background:#FFFFFF; border:2px solid #6C63FF;
                border-radius:18px; padding:2rem; margin-bottom:1.5rem; text-align:center;
                box-shadow:0 2px 16px rgba(108,99,255,0.12);">
        <div style="color:#6C63FF; font-size:0.75rem; font-weight:700;
                    letter-spacing:2px; text-transform:uppercase; margin-bottom:0.5rem;">
            Your Next Skill to Learn
        </div>
        <div style="font-size:2.8rem; font-weight:700; color:#1D1D1F; margin-bottom:0.75rem;">
            {next_skill_name}
        </div>
        <div style="background:#F0EFFF; border-radius:8px; padding:0.65rem 1.25rem;
                    display:inline-block; color:#86868B; font-size:1rem;">
            Appears in <strong style="color:#6C63FF;">{next_skill_freq:.1f}%</strong>
            of <strong style="color:#1D1D1F;">{best_track}</strong> job postings in the Indian market
        </div>
        <div style="color:#86868B; font-size:0.9rem; margin-top:1rem;
                    max-width:600px; margin-left:auto; margin-right:auto; line-height:1.6;">
            {next_skill_why}
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.success(
        f"You already have all required skills for **{best_track}**. "
        "Focus on deepening your existing skills to Advanced level."
    )

# ── Readiness Gauge ───────────────────────────────────────────
st.subheader("Placement Readiness Score")
st.markdown(
    "This score is a weighted average across all required skills for your best track. "
    "Skills appearing more frequently in job postings carry higher weight."
)

gauge_color = (
    "#34C759" if readiness_score >= 70
    else "#FF9500" if readiness_score >= 40
    else "#FF3B30"
)
readiness_label = (
    "Placement Ready"         if readiness_score >= 70
    else "Approaching Readiness" if readiness_score >= 40
    else "Not Yet Ready"
)

fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=readiness_score,
    number={"suffix": "%", "font": {"size": 48, "color": "#1D1D1F"}},
    delta={
        "reference": 70,
        "increasing": {"color": "#34C759"},
        "decreasing": {"color": "#FF3B30"},
        "suffix": "% from readiness threshold",
    },
    gauge={
        "axis": {
            "range": [0, 100],
            "tickcolor": "#86868B",
            "tickfont": {"color": "#86868B"},
        },
        "bar": {"color": gauge_color},
        "bgcolor": "#F5F5F7",
        "bordercolor": "#D2D2D7",
        "steps": [
            {"range": [0,  40], "color": "rgba(255, 59, 48, 0.08)"},
            {"range": [40, 70], "color": "rgba(255, 149, 0, 0.08)"},
            {"range": [70, 100], "color": "rgba(52, 199, 89, 0.08)"},
        ],
        "threshold": {
            "line": {"color": "#1D1D1F", "width": 2},
            "thickness": 0.85,
            "value": 70,
        },
    },
    title={
        "text": readiness_label,
        "font": {"size": 18, "color": gauge_color},
    },
))
fig_gauge.update_layout(
    paper_bgcolor="#FFFFFF",
    font=dict(color="#1D1D1F"),
    height=360,
    margin=dict(l=40, r=40, t=60, b=20),
)

col_gauge, col_meaning = st.columns([2, 1])
with col_gauge:
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_meaning:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:#FFFFFF; border:1px solid #D2D2D7; border-radius:14px; padding:1.25rem;">
        <div style="color:#86868B; font-size:0.75rem; font-weight:600; text-transform:uppercase;">
            Your Score
        </div>
        <div style="font-size:2.5rem; font-weight:700; color:{gauge_color};">
            {readiness_score}%
        </div>
        <div style="color:#1D1D1F; font-weight:600;">{readiness_label}</div>
        <hr style="border:none; border-top:1px solid #D2D2D7; margin:0.75rem 0;">
        <div style="color:#86868B; font-size:0.85rem; line-height:1.7;">
            <strong style="color:#1D1D1F;">Target:</strong> 70% or above<br><br>
            <span style="color:#FF3B30;">Below 40%</span> — Not competitive<br>
            <span style="color:#FF9500;">40–70%</span> — Approaching readiness<br>
            <span style="color:#34C759;">70% and above</span> — Placement ready
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Priority Queue ────────────────────────────────────────────
st.subheader(f"Full Skill Priority Queue for {best_track}")
st.markdown(
    "Missing skills ranked by how frequently they appear in Indian job postings. "
    "Learn them in this order."
)

best_match_data = career_matches[0] if career_matches else {}
missing_skills  = best_match_data.get("missing_skills", [])

if missing_skills:
    priority_list = missing_skills[:10]

    for rank, ms in enumerate(priority_list, start=1):
        skill_name = ms.get("skill", "Unknown")
        freq       = ms.get("frequency_pct", 0.0)

        rank_color = (
            "#FF3B30" if rank == 1
            else "#FF9500" if rank <= 3
            else "#6C63FF"
        )
        is_next = (rank == 1 and next_skill_info)
        badge   = "  — Start Here" if is_next else ""

        st.markdown(f"""
        <div style="background:#FFFFFF; border:1px solid #D2D2D7; border-radius:10px;
                    padding:0.85rem 1rem; margin:0.3rem 0;
                    border-left:4px solid {rank_color};">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span style="color:{rank_color}; font-weight:700; font-size:1rem;">
                        #{rank}
                    </span>
                    <span style="color:#1D1D1F; font-weight:600; margin-left:0.75rem;">
                        {skill_name}
                    </span>
                    <span style="color:#FF9500; font-size:0.8rem; font-weight:600;">
                        {badge}
                    </span>
                </div>
                <div style="color:#86868B; font-size:0.9rem;">
                    {freq:.1f}% of job postings
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.success(
        f"You already have all required skills for **{best_track}**. "
        "No missing skills found in the priority queue."
    )

st.markdown("---")

# ── Navigation ────────────────────────────────────────────────
col_prev, col_next = st.columns(2)
with col_prev:
    if st.button("Back — Career Track Match", use_container_width=True):
        st.switch_page("pages/05_career_match.py")
with col_next:
    if st.button("Next — Peer Mirror", type="primary", use_container_width=True):
        st.switch_page("pages/07_peer_mirror.py")
