# pages/10_final_report.py — Window 10: Final Summary & Download

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from brain import generate_student_report_csv, CAREER_TRACKS
from _sidebar import APPLE_CSS, render_sidebar

st.set_page_config(
    page_title="SkillDrift — Final Report",
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

student_name    = st.session_state.get("student_name", "")
semester        = st.session_state.get("semester", "?")
drift_score     = st.session_state.get("drift_score")     or 0
drift_label     = st.session_state.get("drift_label")     or ""
entropy_score   = st.session_state.get("entropy_score")   or 0
entropy_label   = st.session_state.get("entropy_label")   or ""
best_track      = st.session_state.get("best_track",      "Unknown")
match_pct       = st.session_state.get("match_pct",       0)
readiness_score = st.session_state.get("readiness_score") or 0
next_skill_info = st.session_state.get("next_skill_info", {})
urgency_info    = st.session_state.get("urgency_info",    {})
focus_debt_info = st.session_state.get("focus_debt_info", {})
peer_info       = st.session_state.get("peer_info",       {})
verified_skills = st.session_state.get("verified_skills", {})
career_matches  = st.session_state.get("career_matches",  [])

next_skill       = next_skill_info.get("skill", "N/A")         if next_skill_info else "N/A"
urgency_level    = urgency_info.get("urgency_level", "Unknown") if urgency_info    else "Unknown"
urgency_color    = urgency_info.get("urgency_color", "#6C63FF") if urgency_info    else "#6C63FF"
focus_debt_hours = focus_debt_info.get("focus_debt_hours", 0)  if focus_debt_info else 0
days_to_recover  = focus_debt_info.get("days_to_recover", 0)   if focus_debt_info else 0

# Map urgency colors to Apple palette
URGENCY_COLOR_MAP = {
    "Green":  "#34C759",
    "Yellow": "#FF9500",
    "Red":    "#FF3B30",
}
urgency_color = URGENCY_COLOR_MAP.get(urgency_level, "#6C63FF")

today_str = datetime.now().strftime("%Y-%m-%d")

st.title("Your SkillDrift Report Card")
st.markdown(
    "Everything SkillDrift calculated about your career readiness — "
    "in one place. Download it and share it with your placement cell."
)
st.markdown("---")

# ── Identity Card ─────────────────────────────────────────────
st.markdown(f"""
<div style="background:#FFFFFF; border:2px solid #6C63FF;
            border-radius:18px; padding:1.5rem;
            box-shadow:0 2px 16px rgba(108,99,255,0.1); margin-bottom:1.5rem;">
    <div style="display:flex; align-items:center; gap:1.25rem;">
        <div style="width:64px; height:64px; border-radius:50%; background:#F0EFFF;
                    display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg width="40" height="40" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
                <circle cx="40" cy="30" r="15" fill="#6C63FF"/>
                <ellipse cx="40" cy="65" rx="22" ry="15" fill="#6C63FF"/>
            </svg>
        </div>
        <div>
            <div style="font-size:1.6rem; font-weight:700; color:#1D1D1F;">{student_name}</div>
            <div style="color:#86868B; font-size:0.95rem; margin-top:0.2rem;">
                Semester {semester} &nbsp;|&nbsp; Report generated {today_str}
            </div>
            <div style="color:#6C63FF; font-size:0.85rem; margin-top:0.15rem;">
                SkillDrift Career Focus Analyzer
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Summary Rows ──────────────────────────────────────────────
st.subheader("Complete Analysis Summary")

col_left, col_right = st.columns(2, gap="large")

def report_row(label: str, value: str, value_color: str = "#1D1D1F") -> str:
    return f"""
    <div style="background:#FFFFFF; border:1px solid #D2D2D7; border-radius:10px;
                padding:0.8rem 1rem; margin:0.3rem 0;
                display:flex; justify-content:space-between; align-items:center;">
        <div style="color:#86868B; font-size:0.88rem;">{label}</div>
        <div style="color:{value_color}; font-weight:700; font-size:0.9rem;
                    text-align:right; max-width:55%;">{value}</div>
    </div>
    """

ds_color = (
    "#34C759" if drift_score <= 20
    else "#FF9500" if drift_score <= 60
    else "#FF3B30"
)
es_color = (
    "#34C759" if entropy_score < 1.2
    else "#FF9500" if entropy_score < 2.0
    else "#FF3B30"
)
rs_color = (
    "#34C759" if readiness_score >= 70
    else "#FF9500" if readiness_score >= 40
    else "#FF3B30"
)

with col_left:
    st.markdown("**Skill Analysis**")
    st.markdown(
        report_row("Drift Score",     f"{drift_score} — {drift_label}",     ds_color),
        unsafe_allow_html=True,
    )
    st.markdown(
        report_row("Entropy Score",   f"{entropy_score} bits — {entropy_label}", es_color),
        unsafe_allow_html=True,
    )
    st.markdown(
        report_row("Verified Skills", f"{len(verified_skills)} skills confirmed"),
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Career Match**")
    st.markdown(
        report_row("Best Career Track", best_track, "#6C63FF"),
        unsafe_allow_html=True,
    )
    st.markdown(
        report_row("Match Percentage",  f"{match_pct}%", "#6C63FF"),
        unsafe_allow_html=True,
    )
    st.markdown(
        report_row("Readiness Score",   f"{readiness_score}%", rs_color),
        unsafe_allow_html=True,
    )

with col_right:
    st.markdown("**Action Plan**")
    st.markdown(
        report_row("Next Skill to Learn", next_skill, "#FF9500"),
        unsafe_allow_html=True,
    )
    st.markdown(
        report_row("Urgency Level", urgency_level, urgency_color),
        unsafe_allow_html=True,
    )
    st.markdown(
        report_row(
            "Focus Debt",
            f"{focus_debt_hours} hrs ({days_to_recover} days at 2 hrs/day)",
            "#FF3B30" if focus_debt_hours > 60 else "#FF9500",
        ),
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Top Missing Skills**")

    best_match_data = career_matches[0] if career_matches else {}
    missing_skills  = best_match_data.get("missing_skills", [])

    if missing_skills:
        for i, ms in enumerate(missing_skills[:5], start=1):
            st.markdown(
                report_row(
                    f"#{i} Missing Skill",
                    f"{ms['skill']} ({ms['frequency_pct']:.1f}% of JDs)",
                    "#FF3B30",
                ),
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            report_row("Missing Skills", "None — All required skills verified", "#34C759"),
            unsafe_allow_html=True,
        )

st.markdown("---")

# ── Verified Skill Profile ────────────────────────────────────
st.subheader("Your Verified Skill Profile")

if verified_skills:
    quiz_results = st.session_state.get("quiz_results", [])
    status_map   = {r["skill"]: r["status"] for r in quiz_results} if quiz_results else {}

    skill_rows = []
    for skill, level in verified_skills.items():
        status      = status_map.get(skill, "Confirmed")
        status_label = {
            "Confirmed":  "Confirmed",
            "Downgraded": "Downgraded",
            "Unverified": "Unverified",
        }.get(status, "Confirmed")
        skill_rows.append({
            "Skill":          skill,
            "Verified Level": level,
            "Quiz Status":    status_label,
        })

    skill_df = pd.DataFrame(skill_rows)
    st.dataframe(skill_df, use_container_width=True, hide_index=True)
else:
    st.warning("No verified skills found in this session.")

st.markdown("---")

# ── Download ──────────────────────────────────────────────────
st.subheader("Download Your Report")

session_data = {
    "student_name":    student_name,
    "semester":        semester,
    "drift_score":     drift_score,
    "drift_label":     drift_label,
    "entropy_score":   entropy_score,
    "entropy_label":   entropy_label,
    "best_track":      best_track,
    "match_pct":       match_pct,
    "readiness_score": readiness_score,
    "next_skill":      next_skill,
    "urgency_level":   urgency_level,
    "focus_debt_hours": focus_debt_hours,
    "verified_skills": verified_skills,
}

csv_string    = generate_student_report_csv(session_data)
csv_bytes     = csv_string.encode("utf-8")
name_for_file = student_name.strip().replace(" ", "_")
date_for_file = datetime.now().strftime("%Y_%m_%d")
filename      = f"SkillDrift_Report_{name_for_file}_{date_for_file}.csv"

col_dl, col_info = st.columns([2, 3])

with col_dl:
    st.download_button(
        label="Download My Report as CSV",
        data=csv_bytes,
        file_name=filename,
        mime="text/csv",
        use_container_width=True,
        type="primary",
    )

with col_info:
    st.markdown("""
    <div style="background:#FFFFFF; border:1px solid #D2D2D7;
                border-radius:12px; padding:1rem; font-size:0.9rem; color:#86868B;
                line-height:1.7;">
        <strong style="color:#1D1D1F;">What to do with this file:</strong><br><br>
        Email it to your college placement cell<br>
        Upload it to the Faculty Dashboard when your HOD requests it<br>
        Share it with your mentor or career advisor<br>
        Keep a copy for your own reference
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Quick Share Summary ───────────────────────────────────────
st.subheader("Quick Share Summary")
st.markdown("Copy this text and paste it anywhere — email, WhatsApp, or Telegram.")

peer_rate = peer_info.get("student_placement_rate", "N/A") if peer_info else "N/A"

plain_summary = f"""SkillDrift Career Report — {student_name}
Generated: {today_str}

Student Name   : {student_name}
Semester       : {semester}

SKILL ANALYSIS
Drift Score    : {drift_score} / 100 ({drift_label})
Entropy Score  : {entropy_score} bits ({entropy_label})
Verified Skills: {len(verified_skills)}

CAREER MATCH
Best Track     : {best_track}
Match %        : {match_pct}%
Readiness      : {readiness_score}%

ACTION PLAN
Next Skill     : {next_skill}
Urgency        : {urgency_level}
Focus Debt     : {focus_debt_hours} hours

Est. Placement Rate (current profile): {peer_rate}%

Generated by SkillDrift — Career Focus Analyzer for B.Tech CSE Students"""

st.code(plain_summary, language=None)

st.markdown("---")

# ── What Happens Next ─────────────────────────────────────────
st.subheader("What Should You Do Next?")

if readiness_score >= 70:
    st.success(
        f"You are approaching placement readiness for {best_track}. "
        f"Your readiness score of {readiness_score}% puts you ahead of most peers. "
        f"Focus on deepening your top skills to Advanced level and building one "
        f"complete project that demonstrates end-to-end capability in {best_track}."
    )
elif readiness_score >= 40:
    st.warning(
        f"You are partially ready for {best_track} roles. "
        f"Your readiness score of {readiness_score}% means you have a foundation "
        f"but significant gaps remain. "
        f"Start with **{next_skill}** today — it appears in the highest percentage "
        f"of job postings for your target track. "
        f"Stop learning new technologies until your readiness score crosses 70%."
    )
else:
    st.error(
        f"Your readiness score of {readiness_score}% requires urgent action. "
        f"You are not yet competitive for {best_track} placements at your current trajectory. "
        f"Your most important step: open a free course on **{next_skill}** "
        f"and commit to studying it for the next 30 days exclusively. "
        f"Share this report with your mentor and placement cell immediately."
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── Navigation ────────────────────────────────────────────────
col_prev, col_restart = st.columns(2)
with col_prev:
    if st.button("Back — Market Intelligence", use_container_width=True):
        st.switch_page("pages/08_market_intel.py")
with col_restart:
    if st.button("Start a New Analysis", use_container_width=True):
        keys_to_clear = [
            "student_name", "semester", "selected_skills", "verified_skills",
            "quiz_results", "quiz_complete", "drift_score", "drift_label",
            "track_counts", "entropy_score", "entropy_label", "career_matches",
            "best_track", "match_pct", "readiness_score", "next_skill_info",
            "urgency_info", "focus_debt_info", "peer_info", "session_start",
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.switch_page("pages/02_skill_input.py")
