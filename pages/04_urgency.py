# pages/04_urgency.py — Window 4: Urgency Engine

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from brain import CAREER_TRACKS
from _sidebar import APPLE_CSS, render_sidebar

st.set_page_config(
    page_title="SkillDrift — Urgency Engine",
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

st.title("Urgency Engine")
st.markdown("How much time do you have left — and how much have you already lost?")
st.markdown("---")

urgency_info    = st.session_state.get("urgency_info", {})
focus_debt_info = st.session_state.get("focus_debt_info", {})
semester        = st.session_state.get("semester", 4)
best_track      = st.session_state.get("best_track", "your best matching track")

if not urgency_info:
    st.warning("Urgency data not found. Please complete the quiz first.")
    st.stop()

urgency_level   = urgency_info.get("urgency_level", "Red")
urgency_color   = urgency_info.get("urgency_color", "#FF3B30")
urgency_message = urgency_info.get("urgency_message", "")
days_remaining  = urgency_info.get("days_remaining", 0)
weeks_remaining = urgency_info.get("weeks_remaining", 0)

# Map to Apple-style colors
URGENCY_COLOR_MAP = {
    "Green":  "#34C759",
    "Yellow": "#FF9500",
    "Red":    "#FF3B30",
}
urgency_color = URGENCY_COLOR_MAP.get(urgency_level, "#FF3B30")

# ── Urgency Banner ────────────────────────────────────────────
level_labels = {"Green": "Low Urgency", "Yellow": "Moderate Urgency", "Red": "High Urgency"}
level_display = level_labels.get(urgency_level, urgency_level)

st.markdown(f"""
<div style="background:{urgency_color}18; border:2px solid {urgency_color};
            border-radius:14px; padding:1.5rem; margin-bottom:1.5rem;">
    <div style="font-size:1.3rem; font-weight:700; color:{urgency_color};">
        {level_display}
    </div>
    <div style="color:#1D1D1F; font-size:1rem; margin-top:0.5rem; line-height:1.6;">
        {urgency_message}
    </div>
</div>
""", unsafe_allow_html=True)

# ── Countdown Cards ───────────────────────────────────────────
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown(f"""
    <div style="background:#FFFFFF; border:1px solid #D2D2D7; border-radius:14px;
                padding:1.5rem; text-align:center; box-shadow:0 2px 8px rgba(0,0,0,0.04);">
        <div style="color:#86868B; font-size:0.75rem; font-weight:600;
                    letter-spacing:1px; text-transform:uppercase;">Your Semester</div>
        <div style="font-size:3rem; font-weight:700; color:#6C63FF; margin:0.35rem 0;">
            {semester}
        </div>
        <div style="color:#86868B; font-size:0.9rem;">of 8 semesters</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if semester >= 7:
        countdown_text = "Active"
        countdown_sub  = "Placement season is here"
    else:
        countdown_text = str(weeks_remaining)
        countdown_sub  = "weeks until Semester 7"

    st.markdown(f"""
    <div style="background:#FFFFFF; border:1px solid #D2D2D7; border-radius:14px;
                padding:1.5rem; text-align:center; box-shadow:0 2px 8px rgba(0,0,0,0.04);">
        <div style="color:#86868B; font-size:0.75rem; font-weight:600;
                    letter-spacing:1px; text-transform:uppercase;">Time Remaining</div>
        <div style="font-size:3rem; font-weight:700; color:{urgency_color}; margin:0.35rem 0;">
            {countdown_text}
        </div>
        <div style="color:#86868B; font-size:0.9rem;">{countdown_sub}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    debt_hours = focus_debt_info.get("focus_debt_hours", 0)
    debt_color = (
        "#FF3B30" if debt_hours > 90
        else "#FF9500" if debt_hours > 30
        else "#34C759"
    )

    st.markdown(f"""
    <div style="background:#FFFFFF; border:1px solid #D2D2D7; border-radius:14px;
                padding:1.5rem; text-align:center; box-shadow:0 2px 8px rgba(0,0,0,0.04);">
        <div style="color:#86868B; font-size:0.75rem; font-weight:600;
                    letter-spacing:1px; text-transform:uppercase;">Focus Debt</div>
        <div style="font-size:3rem; font-weight:700; color:{debt_color}; margin:0.35rem 0;">
            {debt_hours}
        </div>
        <div style="color:#86868B; font-size:0.9rem;">estimated hours off-track</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Focus Debt Explanation ────────────────────────────────────
st.subheader("Your Focus Debt Explained")

daily_hours        = focus_debt_info.get("daily_hours", 2)
days_to_recover    = focus_debt_info.get("days_to_recover", 0)
distraction_skills = focus_debt_info.get("distraction_skills", [])
on_track_skills    = focus_debt_info.get("on_track_skills", [])

st.markdown(f"""
<div style="background:#FFFFFF; border:1px solid #D2D2D7; border-radius:14px;
            padding:1.5rem; color:#1D1D1F; line-height:1.7; margin-bottom:1rem;">
    Your <strong>Focus Debt</strong> is the estimated hours spent learning skills that do not
    contribute to your best matching career track: <strong>{best_track}</strong>.<br><br>
    Each off-track skill is estimated at <strong>30 hours</strong> of learning time
    (based on average free course lengths on YouTube and NPTEL).<br><br>
    <span style="background:#F5F5F7; border-radius:8px; padding:0.5rem 0.75rem;
                 display:block; border-left:3px solid {debt_color};">
        Focus debt: <strong>{debt_hours} hours</strong>.
        At {daily_hours} hours of focused study per day,
        that is <strong>{days_to_recover} days</strong> of learning time redirected
        away from your career goal.
    </span>
</div>
""", unsafe_allow_html=True)

# ── Skill Breakdown ───────────────────────────────────────────
st.markdown("---")
col_a, col_b = st.columns(2, gap="medium")

with col_a:
    st.markdown(f"**On-Track Skills for {best_track}**")
    if on_track_skills:
        for skill in on_track_skills:
            st.markdown(
                f"<div style='background:#FFFFFF; border:1px solid #D2D2D7; "
                f"border-left:4px solid #34C759; border-radius:8px; "
                f"padding:0.4rem 0.8rem; margin:0.2rem 0; color:#1D1D1F;'>"
                f"{skill}</div>",
                unsafe_allow_html=True,
            )
    else:
        st.info("None of your verified skills match the required list for this track.")

with col_b:
    st.markdown("**Off-Track Skills (Focus Debt)**")
    if distraction_skills:
        for skill in distraction_skills:
            st.markdown(
                f"<div style='background:#FFFFFF; border:1px solid #D2D2D7; "
                f"border-left:4px solid #FF3B30; border-radius:8px; "
                f"padding:0.4rem 0.8rem; margin:0.2rem 0; color:#1D1D1F;'>"
                f"{skill} — 30 hrs estimated</div>",
                unsafe_allow_html=True,
            )
    else:
        st.success("All your verified skills are on-track. No focus debt detected.")

st.markdown("---")

# ── Focus Debt vs Available Time Chart ───────────────────────
st.subheader("Focus Debt vs Available Study Time")

semesters_remaining = max(0, 8 - semester)
available_hours = semesters_remaining * 20 * 5 * daily_hours

fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(
    name="Focus Debt (hours off-track)",
    x=["Your Situation"],
    y=[debt_hours],
    marker_color="#FF3B30",
    text=[f"{debt_hours} hrs"],
    textposition="outside",
    textfont=dict(color="#1D1D1F"),
))
fig_bar.add_trace(go.Bar(
    name="Available Focused Study Hours Remaining",
    x=["Your Situation"],
    y=[available_hours],
    marker_color="#34C759",
    text=[f"{available_hours} hrs"],
    textposition="outside",
    textfont=dict(color="#1D1D1F"),
))
fig_bar.update_layout(
    barmode="group",
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#F5F5F7",
    font=dict(color="#1D1D1F"),
    legend=dict(
        bgcolor="#FFFFFF",
        bordercolor="#D2D2D7",
        borderwidth=1,
        font=dict(color="#1D1D1F"),
    ),
    yaxis=dict(gridcolor="#D2D2D7", title="Hours", color="#1D1D1F"),
    xaxis=dict(gridcolor="#D2D2D7", color="#1D1D1F"),
    margin=dict(t=40, b=40),
    height=360,
)
st.plotly_chart(fig_bar, use_container_width=True)
st.caption(
    f"Available hours: {semesters_remaining} semesters × 20 weeks × 5 days "
    f"× {daily_hours} hrs/day = {available_hours} hrs"
)

# ── Distraction Skills Table ──────────────────────────────────
if distraction_skills:
    st.markdown("---")
    st.subheader("Off-Track Skills Breakdown")

    dist_df = pd.DataFrame([
        {
            "Skill":                  skill,
            "Estimated Hours Spent":  30,
            "Relevant to Best Track": "No",
            "Recommendation":         "Deprioritise — focus on your career track first",
        }
        for skill in distraction_skills
    ])
    st.dataframe(dist_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ── Navigation ────────────────────────────────────────────────
col_prev, col_next = st.columns(2)
with col_prev:
    if st.button("Back — Drift Score", use_container_width=True):
        st.switch_page("pages/03_drift_score.py")
with col_next:
    if st.button("Next — Career Track Match", type="primary", use_container_width=True):
        st.switch_page("pages/05_career_match.py")
