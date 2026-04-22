# pages/07_peer_mirror.py — Window 7: Peer Mirror & Survival Rate

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from brain import CAREER_TRACKS, FOCUSED_PLACEMENT_RATES, TRACK_SURVIVAL_RATES
from _sidebar import APPLE_CSS, render_sidebar

st.set_page_config(
    page_title="SkillDrift — Peer Mirror",
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

st.title("Peer Mirror & Survival Rate")
st.markdown(
    "What typically happens to students with a skill profile like yours "
    "when placement season arrives?"
)

st.info(
    "Data Disclaimer: All placement rates and survival rates shown on this page are "
    "estimates based on general industry skill-depth research from NASSCOM annual reports "
    "and AICTE published outcome data. They are not exact figures for specific drift score ranges. "
    "The Drift Score is the mathematically defensible output. "
    "These rates provide contextual support.",
)

st.markdown("---")

peer_info    = st.session_state.get("peer_info", {})
drift_score  = st.session_state.get("drift_score") or 0
drift_label  = st.session_state.get("drift_label", "")
best_track   = st.session_state.get("best_track", "Unknown")
student_name = st.session_state.get("student_name", "You")

if not peer_info:
    st.warning("Peer data not found. Please complete the quiz first.")
    st.stop()

student_rate   = peer_info.get("student_placement_rate", 0)
focused_rate   = peer_info.get("focused_placement_rate", 0)
survival_rates = peer_info.get("survival_rates", TRACK_SURVIVAL_RATES)

# ── Two Hero Metric Cards ─────────────────────────────────────
col_you, col_focused = st.columns(2, gap="medium")

rate_color = (
    "#34C759" if student_rate >= 60
    else "#FF9500" if student_rate >= 40
    else "#FF3B30"
)

with col_you:
    st.markdown(f"""
    <div style="background:#FFFFFF; border:2px solid {rate_color};
                border-radius:18px; padding:2rem; text-align:center;
                box-shadow:0 2px 12px rgba(0,0,0,0.06);">
        <div style="color:#86868B; font-size:0.75rem; font-weight:600;
                    letter-spacing:1px; text-transform:uppercase;">
            Your Estimated Placement Rate
        </div>
        <div style="font-size:4rem; font-weight:700; color:{rate_color}; margin:0.5rem 0;">
            {student_rate}%
        </div>
        <div style="color:#86868B; font-size:0.9rem;">
            Students with Drift Score {drift_score} ({drift_label})
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_focused:
    st.markdown(f"""
    <div style="background:#FFFFFF; border:2px solid #34C759;
                border-radius:18px; padding:2rem; text-align:center;
                box-shadow:0 2px 12px rgba(0,0,0,0.06);">
        <div style="color:#86868B; font-size:0.75rem; font-weight:600;
                    letter-spacing:1px; text-transform:uppercase;">
            Focused {best_track} Student Rate
        </div>
        <div style="font-size:4rem; font-weight:700; color:#34C759; margin:0.5rem 0;">
            {focused_rate}%
        </div>
        <div style="color:#86868B; font-size:0.9rem;">
            Students focused on {best_track} from early semesters
        </div>
    </div>
    """, unsafe_allow_html=True)

gap = focused_rate - student_rate
if gap > 0:
    st.markdown(f"""
    <div style="background:#FF3B3010; border:1px solid #FF3B30;
                border-radius:10px; padding:1rem; text-align:center; margin-top:1rem;">
        <span style="color:#FF3B30; font-size:1.1rem; font-weight:700;">
            The focus gap costs you {gap} percentage points in estimated placement probability.
        </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Side-by-Side Bar Charts ───────────────────────────────────
col_chart1, col_chart2 = st.columns(2, gap="medium")

with col_chart1:
    st.subheader("Placement Rate Comparison")

    fig_placement = go.Figure()
    fig_placement.add_trace(go.Bar(
        name="Your Estimated Rate",
        x=["Your Profile"],
        y=[student_rate],
        marker_color=rate_color,
        text=[f"{student_rate}%"],
        textposition="outside",
        textfont=dict(color="#1D1D1F"),
    ))
    fig_placement.add_trace(go.Bar(
        name=f"Focused {best_track} Students",
        x=[f"Focused {best_track}"],
        y=[focused_rate],
        marker_color="#34C759",
        text=[f"{focused_rate}%"],
        textposition="outside",
        textfont=dict(color="#1D1D1F"),
    ))
    fig_placement.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F5F5F7",
        font=dict(color="#1D1D1F"),
        yaxis=dict(range=[0, 115], gridcolor="#D2D2D7", title="Placement Rate (%)", color="#1D1D1F"),
        xaxis=dict(gridcolor="#D2D2D7", color="#1D1D1F"),
        legend=dict(bgcolor="#FFFFFF", bordercolor="#D2D2D7", borderwidth=1),
        margin=dict(t=20, b=20),
        height=340,
        showlegend=False,
    )
    st.plotly_chart(fig_placement, use_container_width=True)

with col_chart2:
    st.subheader("Survival Rate by Career Track")
    st.caption(
        "Percentage of students who commit to a track and reach "
        "placement readiness by Semester 8"
    )

    tracks_s  = list(survival_rates.keys())
    rates_s   = list(survival_rates.values())
    bar_colors_s = [
        "#6C63FF" if t == best_track else "#D2D2D7"
        for t in tracks_s
    ]

    fig_survival = go.Figure(go.Bar(
        x=rates_s,
        y=tracks_s,
        orientation="h",
        marker_color=bar_colors_s,
        text=[f"{r}%" for r in rates_s],
        textposition="outside",
        textfont=dict(color="#1D1D1F"),
    ))
    fig_survival.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F5F5F7",
        font=dict(color="#1D1D1F"),
        xaxis=dict(range=[0, 115], gridcolor="#D2D2D7", title="Survival Rate (%)", color="#1D1D1F"),
        yaxis=dict(gridcolor="#D2D2D7", color="#1D1D1F"),
        margin=dict(t=20, b=20, l=10, r=50),
        height=340,
    )
    st.plotly_chart(fig_survival, use_container_width=True)

st.markdown("---")

# ── Analysis Text ─────────────────────────────────────────────
st.subheader("What These Numbers Mean for You")

track_survival = survival_rates.get(best_track, 60)

if student_rate >= 60:
    overall_tone = (
        f"Your current profile puts you in a relatively strong position. "
        f"Students with a Drift Score of {drift_score} have an estimated "
        f"placement rate of {student_rate}% — above the average for Indian CSE graduates."
    )
elif student_rate >= 40:
    overall_tone = (
        f"Your current profile shows moderate placement risk. "
        f"Students with a Drift Score of {drift_score} have an estimated "
        f"placement rate of {student_rate}% — below what focused students achieve "
        f"and leaving significant room for improvement."
    )
else:
    overall_tone = (
        f"Your current profile carries high placement risk. "
        f"Students with a Drift Score of {drift_score} have an estimated "
        f"placement rate of only {student_rate}% — nearly half the rate of "
        f"focused students in your recommended track."
    )

track_tone = (
    f"**{best_track}** has a survival rate of **{track_survival}%**, "
    f"meaning {track_survival} out of every 100 students who commit to this track "
    f"early enough reach placement readiness by Semester 8. "
)

if track_survival >= 70:
    track_tone += "This is one of the more achievable tracks — strong demand and learnable skills."
elif track_survival >= 55:
    track_tone += (
        "This track is achievable with consistent effort but requires focus "
        "from this semester onwards."
    )
else:
    track_tone += (
        "This track requires deep mathematical and technical foundations. "
        "Starting late significantly reduces your probability of reaching readiness. "
        "Consider whether an adjacent track with a higher survival rate might be more strategic."
    )

action_tone = (
    f"\n\nThe difference between your estimated {student_rate}% and the "
    f"focused student rate of {focused_rate}% is not talent — it is "
    f"time and deliberate focus. Every additional semester of drift "
    f"reduces that gap's recoverability."
)

st.markdown(overall_tone + "\n\n" + track_tone + action_tone)

st.markdown("---")

# ── Lookup Table ──────────────────────────────────────────────
with st.expander("View Full Placement Rate Lookup Table (All Drift Score Ranges)"):
    st.markdown(
        "These estimates are based on general industry skill-depth research. "
        "They are labeled as estimates throughout this platform."
    )
    lookup_data = [
        {"Drift Score Range": "0 – 20",   "Label": "Highly Focused",      "Est. Placement Rate": "78%"},
        {"Drift Score Range": "20 – 40",  "Label": "Moderately Focused",  "Est. Placement Rate": "62%"},
        {"Drift Score Range": "40 – 60",  "Label": "Drifting",            "Est. Placement Rate": "44%"},
        {"Drift Score Range": "60 – 80",  "Label": "Highly Scattered",    "Est. Placement Rate": "29%"},
        {"Drift Score Range": "80 – 100", "Label": "Extremely Scattered", "Est. Placement Rate": "18%"},
    ]
    st.dataframe(pd.DataFrame(lookup_data), use_container_width=True, hide_index=True)

st.markdown("---")

# ── Navigation ────────────────────────────────────────────────
col_prev, col_next = st.columns(2)
with col_prev:
    if st.button("Back — Next Skill", use_container_width=True):
        st.switch_page("pages/06_next_skill.py")
with col_next:
    if st.button("Next — Market Intelligence", type="primary", use_container_width=True):
        st.switch_page("pages/08_market_intel.py")
