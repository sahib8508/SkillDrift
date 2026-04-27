# pages/03_drift_score.py
# =============================================================
# Result dashboard - first page after Submit Test.
#
# Shows only:
#   1. Final score (overall percentage)
#   2. Per-skill verification status (Confirmed / Borderline /
#      Not Verified) - no question-wise correctness, no answer
#      keys, no "you got Q3 wrong" details.
#   3. Drift / Entropy metric cards as the analytical view.
# =============================================================

import streamlit as st
import pandas as pd

from session_store import init_session
from brain import CAREER_TRACKS
from _sidebar import APPLE_CSS, render_sidebar

st.set_page_config(
    page_title="SkillDrift - Result",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session()

st.session_state["_current_page"] = "drift"
st.markdown(APPLE_CSS, unsafe_allow_html=True)
render_sidebar()

if not st.session_state.get("student_name"):
    st.warning("Session not found. Please start from the beginning.")
    if st.button("Go to Skill Input"):
        st.switch_page("pages/02_skill_input.py")
    st.stop()

drift_score     = st.session_state.get("drift_score")   or 0
drift_label     = st.session_state.get("drift_label")   or ""
entropy_score   = st.session_state.get("entropy_score") or 0
entropy_label   = st.session_state.get("entropy_label") or ""
track_counts    = st.session_state.get("track_counts")  or {}
verified_skills = st.session_state.get("verified_skills", {})
quiz_results    = st.session_state.get("quiz_results", [])

if not verified_skills and not quiz_results:
    st.warning("No verified skills found. Please complete the quiz first.")
    if st.button("Go to Quiz"):
        st.switch_page("pages/02_skill_input.py")
    st.stop()

# If quiz done but ALL skills failed — show friendly message
if quiz_results and not verified_skills:
    st.error(
        "⚠️ None of your claimed skills were verified by the quiz. "
        "Your Drift and Entropy scores below are based on your **claimed** skills "
        "for reference, but please retake the quiz with honest self-assessment."
    )
    # Fall back to claimed skills for display purposes only
    for r in quiz_results:
        verified_skills[r["skill"]] = r["claimed_level"]


# =============================================================
# FINAL SCORE
# =============================================================

total_correct   = sum(int(r.get("correct_count", 0))   for r in quiz_results)
total_questions = sum(int(r.get("total_questions", 0)) for r in quiz_results)
final_pct = round((total_correct / total_questions) * 100, 1) if total_questions else 0.0

if   final_pct >= 70: score_label, score_color = "Strong",     "#15803d"
elif final_pct >= 40: score_label, score_color = "Borderline", "#d97706"
else:                 score_label, score_color = "Needs Work", "#ba1a1a"


# =============================================================
# PAGE TITLE
# =============================================================

st.markdown(f"""
<div style="margin-bottom:24px;">
    <div style="font-family:'Manrope',sans-serif;font-size:1.5rem;font-weight:800;color:#171c1f;">
        Your Test Result
    </div>
    <div style="font-size:0.875rem;color:#515f74;margin-top:5px;">
        Final score and skill evaluation for {st.session_state.get('student_name','')}.
    </div>
</div>
""", unsafe_allow_html=True)


# =============================================================
# FINAL SCORE CARD
# =============================================================

st.markdown(f"""
<div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:14px;
            padding:28px 32px;margin-bottom:24px;
            border-top:4px solid {score_color};
            display:flex;align-items:center;justify-content:space-between;
            flex-wrap:wrap;gap:16px;">
  <div>
    <div style="font-size:0.78rem;font-weight:700;color:#515f74;
                text-transform:uppercase;letter-spacing:0.06em;">Final Score</div>
    <div style="font-family:'Manrope',sans-serif;font-size:2.6rem;font-weight:800;
                color:{score_color};line-height:1.1;margin-top:6px;">{final_pct}%</div>
    <div style="font-size:0.85rem;color:#515f74;margin-top:4px;">
      Based on {total_questions} verification question{'s' if total_questions != 1 else ''}
      across {len(quiz_results)} skill{'s' if len(quiz_results) != 1 else ''}.
    </div>
  </div>
  <div style="text-align:right;">
    <div style="font-size:0.78rem;font-weight:700;color:#515f74;
                text-transform:uppercase;letter-spacing:0.06em;">Evaluation</div>
    <div style="font-family:'Manrope',sans-serif;font-size:1.4rem;font-weight:800;
                color:{score_color};margin-top:6px;">{score_label}</div>
    <div style="font-size:0.82rem;color:#515f74;margin-top:4px;">
      Verified skills: <b>{len(verified_skills)}</b> of {len(quiz_results)} passed
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# =============================================================
# SKILL EVALUATION (no per-question details)
# =============================================================

st.markdown("""
<div style="font-family:'Manrope',sans-serif;font-size:1.05rem;font-weight:700;
            color:#171c1f;margin:8px 0 6px 0;">Skill Evaluation</div>
<div style="font-size:0.86rem;color:#515f74;margin-bottom:14px;">
    Status of each skill you claimed. Per-question details are not
    shown to keep the assessment outcome focused.
</div>
""", unsafe_allow_html=True)

if quiz_results:
    rows = []
    for r in quiz_results:
        correct = int(r.get("correct_count", 0))
        total   = int(r.get("total_questions", 0))
        score_str = f"{correct}/{total}" if total > 0 else "—"
        rows.append({
            "Skill":          r.get("skill", ""),
            "Claimed Level":  r.get("claimed_level", ""),
            "Score":          score_str,
            "Verified Level": r.get("verified_level", ""),
            "Status":         r.get("status", ""),
        })
    df = pd.DataFrame(rows)

    def style_status(val: str):
        if val == "Confirmed":     return "color: #15803d; font-weight: 700;"
        if val == "Borderline":    return "color: #d97706; font-weight: 700;"
        if val == "Not Verified":  return "color: #ba1a1a; font-weight: 700;"
        if val == "Unverified":    return "color: #94a3b8;"
        return ""

    def style_score(val: str):
        if "/" not in val:
            return ""
        parts = val.split("/")
        try:
            c, t = int(parts[0]), int(parts[1])
            ratio = c / t if t > 0 else 0
            if ratio >= 0.67:   return "color: #15803d; font-weight: 700;"
            elif ratio >= 0.34: return "color: #d97706; font-weight: 700;"
            else:               return "color: #ba1a1a; font-weight: 700;"
        except Exception:
            return ""

    styled = df.style.map(style_status, subset=["Status"]).map(style_score, subset=["Score"])
    st.dataframe(styled, use_container_width=True, hide_index=True)

    # Explanation below table
    st.markdown("""
    <div style="font-size:0.82rem;color:#515f74;background:#f6fafe;border-radius:8px;
                padding:10px 14px;border-left:3px solid #002c98;margin-top:8px;line-height:1.6;">
        <b>How scoring works:</b> Each skill has 3 questions.
        <span style="color:#15803d;font-weight:700;">2/3 or 3/3 → Confirmed</span> &nbsp;|&nbsp;
        <span style="color:#d97706;font-weight:700;">1/3 → Borderline</span> (level downgraded) &nbsp;|&nbsp;
        <span style="color:#ba1a1a;font-weight:700;">0/3 → Not Verified</span> (excluded from analysis)
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("No skill evaluation data available.")

st.markdown("<hr style='border:none;border-top:1px solid #e2e8f0;margin:28px 0;'>", unsafe_allow_html=True)


# =============================================================
# DRIFT + ENTROPY CARDS (analytical view)
# =============================================================

st.markdown("""
<div style="font-family:'Manrope',sans-serif;font-size:1.05rem;font-weight:700;
            color:#171c1f;margin:0 0 14px 0;">
    Drift Score and Entropy Score
</div>
""", unsafe_allow_html=True)

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
    # Count only truly verified (Confirmed or Borderline), not Not Verified
    truly_verified = sum(
        1 for r in quiz_results
        if r.get("status") in ("Confirmed", "Borderline")
    )
    not_verified_count = len(quiz_results) - truly_verified
    skill_count = len(verified_skills)
    st.markdown(f"""
    <div class="sd-metric" style="border-top:3px solid #002c98;">
        <div class="sd-metric-label">Verified Skills</div>
        <div class="sd-metric-value" style="color:#002c98;">{truly_verified}</div>
        <div style="font-size:0.9rem;font-weight:700;color:#171c1f;margin-top:8px;">of {len(quiz_results)} claimed</div>
        <div class="sd-metric-sub" style="color:#ba1a1a;">{not_verified_count} failed verification</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)


# =============================================================
# INTERPRETATION
# =============================================================

if drift_score <= 20:
    drift_interpretation = "Your skills are concentrated in very few tracks. This is the ideal pattern."
elif drift_score <= 40:
    drift_interpretation = "Mostly concentrated with some spread. Mild drift - manageable if you stay focused."
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
            Your score of <strong>{drift_score}</strong> measures how <em>unevenly</em> your verified
            skills are distributed across 8 CSE career tracks.<br><br>
            It uses <strong>standard deviation</strong>: a high std means one track dominates
            (focused). A low std means skills are spread evenly (scattered).<br><br>
            <strong>0</strong> = Perfectly even spread = Maximum Drift (Scattered)<br>
            <strong>100</strong> = All skills in one track = No Drift (Highly Focused)
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
            Based on Shannon's Information Entropy — measures <em>how many tracks</em>
            you have touched, regardless of which one dominates.<br><br>
            <strong>0 bits</strong> = All skills in exactly 1 track = Perfect focus.<br>
            <strong>3 bits</strong> = Skills spread across all 8 tracks equally = Max disorder.
        </div>
        <div style="background:#fff8e1;border-radius:8px;padding:12px 14px;
                    border-left:3px solid #d97706;margin-top:16px;
                    font-size:0.88rem;color:#515f74;line-height:1.55;">
            <b>⚠️ Why can Drift be "Focused" but Entropy be "Disordered"?</b><br><br>
            These measure <em>different things</em>. Skills like Python and SQL each belong to
            5–7 tracks in the dataset. So even with just 3 skills, your entropy is high
            because 7 out of 8 tracks are non-zero.<br><br>
            <b>Drift</b> asks: <em>Is one track clearly dominant?</em> (Yes → low drift) <br>
            <b>Entropy</b> asks: <em>How many tracks have at least one skill?</em> (Many → high entropy)<br><br>
            Your current score of <b>{entropy_score} bits</b> means you have touched many tracks,
            but Drift ({drift_score}) confirms Data Analyst is still your dominant track.
            Focus deeper on Data Analyst skills to bring both scores down.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border:none;border-top:1px solid #e2e8f0;margin:28px 0;'>", unsafe_allow_html=True)


# =============================================================
# TRACK BREAKDOWN
# =============================================================

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

    styled_track = track_df.style.map(color_focus, subset=["Focus Signal"])
    st.dataframe(styled_track, use_container_width=True, hide_index=True)
else:
    st.info("No track data available. Please complete the quiz first.")

st.markdown("<hr style='border:none;border-top:1px solid #e2e8f0;margin:28px 0;'>", unsafe_allow_html=True)


# =============================================================
# NAV
# =============================================================

col_nav1, col_nav2 = st.columns(2)
with col_nav2:
    if st.button("Next - Urgency Engine", type="primary", use_container_width=True):
        st.switch_page("pages/04_urgency.py")