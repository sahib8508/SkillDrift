# pages/03_drift_score.py

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

st.session_state["_current_page"] = "drift"
st.markdown(APPLE_CSS, unsafe_allow_html=True)
render_sidebar()

if not st.session_state.get("student_name"):
    st.warning("Session not found. Please start from the beginning.")
    st.switch_page("pages/02_skill_input.py")

drift_score     = st.session_state.get("drift_score")   or 0
drift_label     = st.session_state.get("drift_label")   or ""
entropy_score   = st.session_state.get("entropy_score") or 0
entropy_label   = st.session_state.get("entropy_label") or ""
track_counts    = st.session_state.get("track_counts")  or {}
verified_skills = st.session_state.get("verified_skills", {})

if not verified_skills:
    st.warning("No verified skills found. Please go back and complete the quiz.")
    st.stop()

# ── Page title ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:28px;">
    <div style="font-family:'Manrope',sans-serif;font-size:1.5rem;font-weight:800;color:#171c1f;">
        Drift Score &amp; Entropy Score
    </div>
    <div style="font-size:0.875rem;color:#515f74;margin-top:5px;">
        Calculated from your verified skills only. Skills you failed the quiz for are excluded.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Color logic ────────────────────────────────────────────────────────────────
drift_color = (
    "#15803d" if drift_score <= 20
    else "#d97706" if drift_score <= 60
    else "#ba1a1a"
)
entropy_color = (
    "#15803d" if entropy_score < 1.2
    else "#d97706" if entropy_score < 2.0
    else "#ba1a1a"
)

# ── Score cards ────────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    st.markdown(f"""
    <div class="sd-metric" style="border-top:3px solid {drift_color};">
        <div class="sd-metric-label">Drift Score</div>
        <div class="sd-metric-value" style="color:{drift_color};">{drift_score}</div>
        <div style="font-size:0.9rem;font-weight:700;color:#171c1f;margin-top:8px;">{drift_label}</div>
        <div class="sd-metric-sub">0 = Focused &nbsp;|&nbsp; 100 = Scattered</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="sd-metric" style="border-top:3px solid {entropy_color};">
        <div class="sd-metric-label">Entropy Score</div>
        <div class="sd-metric-value" style="color:{entropy_color};">{entropy_score}</div>
        <div style="font-size:0.9rem;font-weight:700;color:#171c1f;margin-top:8px;">{entropy_label}</div>
        <div class="sd-metric-sub">0 bits = Focused &nbsp;|&nbsp; 3 bits = Max Scatter</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    skill_count = len(verified_skills)
    st.markdown(f"""
    <div class="sd-metric" style="border-top:3px solid #002c98;">
        <div class="sd-metric-label">Verified Skills</div>
        <div class="sd-metric-value" style="color:#002c98;">{skill_count}</div>
        <div style="font-size:0.9rem;font-weight:700;color:#171c1f;margin-top:8px;">Skills Confirmed</div>
        <div class="sd-metric-sub">after Gemini verification</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

# ── Interpretation text ────────────────────────────────────────────────────────
if drift_score <= 20:
    drift_interpretation = "Your skills are concentrated in very few tracks. This is the ideal pattern."
elif drift_score <= 40:
    drift_interpretation = "Mostly concentrated with some spread. Mild drift — manageable if you stay focused."
elif drift_score <= 60:
    drift_interpretation = "Visible spread across multiple tracks. Needs correction before placement season."
else:
    drift_interpretation = "Broadly scattered across many unrelated tracks. This is a placement risk."

ca, cb = st.columns(2, gap="large")

with ca:
    st.markdown(f"""
    <div class="sd-card">
        <div style="font-family:'Manrope',sans-serif;font-size:1rem;font-weight:700;color:#171c1f;margin-bottom:12px;">
            What is the Drift Score?
        </div>
        <div style="font-size:0.9rem;color:#171c1f;line-height:1.7;">
            Your score of <strong>{drift_score}</strong> measures how scattered your {skill_count} verified
            skills are across 8 CSE career tracks.<br><br>
            <strong>0</strong> = All skills in one track — fully focused.<br>
            <strong>100</strong> = Skills spread across all 8 tracks — maximum drift.
        </div>
        <div style="background:#f6fafe;border-radius:8px;padding:12px 14px;
                    border-left:3px solid {drift_color};margin-top:16px;
                    font-size:0.88rem;color:#515f74;line-height:1.55;">
            {drift_interpretation}
        </div>
    </div>
    """, unsafe_allow_html=True)

with cb:
    st.markdown(f"""
    <div class="sd-card">
        <div style="font-family:'Manrope',sans-serif;font-size:1rem;font-weight:700;color:#171c1f;margin-bottom:12px;">
            What is the Entropy Score?
        </div>
        <div style="font-size:0.9rem;color:#171c1f;line-height:1.7;">
            Based on Shannon's Information Entropy — a mathematical measure of disorder.<br><br>
            <strong>0 bits</strong> = All skills in one track — perfect focus.<br>
            <strong>~3 bits</strong> = Skills spread equally — maximum disorder.
        </div>
        <div style="background:#f6fafe;border-radius:8px;padding:12px 14px;
                    border-left:3px solid {entropy_color};margin-top:16px;
                    font-size:0.88rem;color:#515f74;line-height:1.55;">
            Your <strong>{entropy_score} bits</strong> puts you in the <strong>{entropy_label}</strong> category.
            Drift Score measures magnitude of spread. Entropy measures how many tracks you have spread into.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border:none;border-top:1px solid #e2e8f0;margin:28px 0;'>", unsafe_allow_html=True)

# ── Track Breakdown ────────────────────────────────────────────────────────────
st.markdown("""
<div style="font-family:'Manrope',sans-serif;font-size:1rem;font-weight:700;color:#171c1f;margin-bottom:5px;">
    Your Skills Across All 8 Career Tracks
</div>
<div style="font-size:0.875rem;color:#515f74;margin-bottom:16px;">
    More skills in one track = less drift = better placement readiness.
</div>
""", unsafe_allow_html=True)

total_skill_count = max(len(verified_skills), 1)

if track_counts:
    track_df = pd.DataFrame([
        {
            "Career Track":     track,
            "Skills You Have":  count,
            "Share of Profile": f"{round(count / total_skill_count * 100, 1)}%",
            "Focus Signal":     (
                "Primary Track" if count == max(track_counts.values()) and count > 0
                else "Secondary" if count > 0
                else "None"
            ),
        }
        for track, count in track_counts.items()
    ])

    if not track_df.empty:
        track_df = track_df.sort_values("Skills You Have", ascending=False).reset_index(drop=True)

    def color_focus(val):
        if val == "Primary Track":
            return "color: #002c98; font-weight: 700"
        elif val == "Secondary":
            return "color: #d97706"
        return "color: #94a3b8"

    styled = track_df.style.map(color_focus, subset=["Focus Signal"])
    st.dataframe(styled, use_container_width=True, hide_index=True)
else:
    st.info("No track data available. Please complete the quiz first.")

st.markdown("<hr style='border:none;border-top:1px solid #e2e8f0;margin:28px 0;'>", unsafe_allow_html=True)

col_nav1, col_nav2 = st.columns(2)
with col_nav2:
    if st.button("Next — Urgency Engine", type="primary", use_container_width=True):
        st.switch_page("pages/04_urgency.py")
