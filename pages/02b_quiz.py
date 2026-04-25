import time
import streamlit as st
import streamlit.components.v1 as components

from gemini_quiz import (
    ensure_quiz_data, score_all, reset_quiz_state,
)
from proctor import (
    render_proctor_camera, get_proctor_snapshot,
    add_tab_switch_violation, add_fullscreen_exit_violation,
    reset_proctor_state,
)
from brain import (
    calculate_drift_score, calculate_entropy, calculate_career_match,
    calculate_readiness_score, get_next_skill, get_urgency_level,
    calculate_focus_debt, get_peer_placement_rate,
)

try:
    from streamlit_autorefresh import st_autorefresh
    HAS_AUTOREFRESH = True
except Exception:
    HAS_AUTOREFRESH = False

try:
    from streamlit_js_eval import streamlit_js_eval
    HAS_JS_EVAL = True
except Exception:
    HAS_JS_EVAL = False


st.set_page_config(
    page_title="SkillDrift — Proctored Quiz",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =============================================================
# GLOBAL CSS — sitewide select/copy block, hide webrtc controls
# once running, blur questions when locked, fix radio layout.
# =============================================================

st.markdown("""
<style>
[data-testid="stSidebarNav"], [data-testid="collapsedControl"],
[data-testid="stExpandSidebar"], [data-testid="stSidebarCollapseButton"],
section[data-testid="stSidebar"], header[data-testid="stHeader"],
.stDeployButton, #MainMenu, footer { display: none !important; }

html, body, .stApp {
  background: #f6fafe;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  -webkit-user-select: none !important;
  -moz-user-select: none !important;
  -ms-user-select: none !important;
  user-select: none !important;
}
.block-container { padding-top: 1rem !important; max-width: 1100px !important; }

input, textarea {
  -webkit-user-select: text !important;
  user-select: text !important;
}

/* === HIDE STREAMLIT-WEBRTC STOP / SELECT-DEVICE BUTTONS WHEN RUNNING ===
   The webrtc widget's buttons are inside [data-testid="stHorizontalBlock"]
   inside [data-testid="component-iframe-container"]. We can't reach into
   the iframe with CSS, but we hide the surrounding device-select form. */
body.cam-running .webrtc-stop-controls { display: none !important; }

/* === FIX SKILL LEVEL RADIO LAYOUT ===
   The horizontal radio for Beginner / Intermediate / Advanced was
   shifting column widths because each option's flex-basis differed.
   Force a fixed-width container with consistent option sizing. */
div[data-testid="stRadio"] > div[role="radiogroup"] {
  display: grid !important;
  grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
  gap: 4px !important;
  width: 100% !important;
}
div[data-testid="stRadio"] > div[role="radiogroup"] > label {
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  font-size: 0.85rem !important;
}

.q-header {
  background: #002c98; color: #fff; border-radius: 12px;
  padding: 16px 22px; display: flex; justify-content: space-between;
  align-items: center; margin-bottom: 16px; flex-wrap: wrap; gap: 8px;
}
.q-header .title {
  font-family: 'Manrope', sans-serif; font-size: 1rem;
  font-weight: 800; letter-spacing: 0.02em;
}
.q-header .sub { font-size: 0.78rem; opacity: 0.85; margin-top: 2px; }
.q-header .vio-badge {
  background: rgba(255,255,255,0.18); border-radius: 18px;
  padding: 6px 16px; font-size: 0.8rem; font-weight: 700;
}
.q-header .vio-badge.warn { background: #ff9500; color: #000; }
.q-header .vio-badge.bad  { background: #ff3b30; color: #fff; }

.q-card {
  background: #fff; border: 1px solid #e2e8f0; border-radius: 10px;
  padding: 14px 18px; margin-top: 18px; margin-bottom: 8px;
}
.q-card .skill {
  font-family: 'Manrope', sans-serif; font-size: 1.05rem;
  font-weight: 800; color: #002c98;
}
.q-card .meta { font-size: 0.8rem; color: #515f74; margin-top: 3px; }

.q-instr {
  font-size: 0.82rem; color: #515f74; margin: 12px 0 18px 0;
  padding: 10px 14px; background: #eef2ff; border-radius: 8px;
  border-left: 3px solid #002c98;
}

.q-fallback-badge {
  background: #fff7ed; color: #9a3412; border: 1px solid #fdba74;
  border-radius: 10px; padding: 2px 10px; font-size: 0.7rem;
  font-weight: 700; margin-left: 8px;
}

.q-terminated {
  background: #fff5f5; border: 1.5px solid #ff3b30; border-radius: 14px;
  padding: 32px; text-align: center; margin: 20px 0;
}
.q-terminated .title {
  font-family: 'Manrope', sans-serif; font-size: 1.6rem;
  font-weight: 800; color: #ba1a1a; margin-bottom: 14px;
}
.q-terminated .body {
  font-size: 0.95rem; color: #515f74; line-height: 1.6;
  margin-bottom: 8px;
}

.lock-overlay {
  background: #002c98; color: #fff; border-radius: 14px;
  padding: 40px 32px; text-align: center; margin: 14px 0 22px 0;
}
.lock-overlay .title {
  font-family: 'Manrope', sans-serif; font-size: 1.4rem;
  font-weight: 800; margin-bottom: 12px;
}
.lock-overlay .body {
  font-size: 0.95rem; line-height: 1.7; opacity: 0.9;
}
.lock-overlay .step {
  display: inline-block; background: rgba(255,255,255,0.12);
  border-radius: 8px; padding: 6px 14px; margin: 4px;
  font-size: 0.85rem;
}

.questions-blur {
  filter: blur(10px) brightness(0.9);
  pointer-events: none;
  user-select: none;
}

.stButton > button {
  border-radius: 8px; border: 1.5px solid #e2e8f0; background: #fff;
  color: #171c1f; font-weight: 600;
}
.stButton > button[kind="primary"] {
  background: #002c98; color: #fff; border-color: #002c98; font-weight: 700;
}
.stButton > button[kind="primary"]:hover { background: #0038bf; }

.start-test-btn button {
  background: #16a34a !important; color: #fff !important;
  border-color: #16a34a !important; font-size: 1rem !important;
  font-weight: 800 !important; padding: 14px !important;
}
.start-test-btn button:hover { background: #15803d !important; }
</style>
""", unsafe_allow_html=True)


# =============================================================
# 1. GUARDS
# =============================================================

if not st.session_state.get("student_name"):
    st.warning("Please enter your name on the previous page first.")
    if st.button("Go Back"):
        st.switch_page("pages/02_skill_input.py")
    st.stop()

if not st.session_state.get("selected_skills"):
    st.warning("Please select your skills first.")
    if st.button("Go Back"):
        st.switch_page("pages/02_skill_input.py")
    st.stop()

if st.session_state.get("quiz_complete"):
    st.success("Quiz already completed. Redirecting to your dashboard.")
    st.switch_page("pages/03_drift_score.py")
    st.stop()


# =============================================================
# 2. TERMINATED SCREEN (check first so we exit cleanly)
# =============================================================

snap = get_proctor_snapshot()
if snap["violations"] >= 3:
    st.session_state["quiz_terminated"] = True

if st.session_state.get("quiz_terminated"):
    try:
        render_proctor_camera(key="skilldrift-proctor-stop",
                              desired_playing=False)
    except Exception:
        pass
    if HAS_JS_EVAL:
        streamlit_js_eval(
            js_expressions="(document.exitFullscreen ? document.exitFullscreen() : null)",
            key="exit_fs_term",
        )
    st.markdown(
        """
        <div class="q-terminated">
          <div class="title">Test Terminated</div>
          <div class="body">
            Your test was terminated due to repeated proctoring violations
            (face not detected, tab/window switching, or fullscreen exit).
          </div>
          <div class="body">
            All session data will be cleared. Restart from the beginning to
            try again.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Restart from Beginning", type="primary",
                     use_container_width=True, key="qz_restart"):
            reset_quiz_state(full=True)
            reset_proctor_state()
            st.switch_page("pages/01_home.py")
    with c2:
        if st.button("Go Back to Home", use_container_width=True,
                     key="qz_goback"):
            reset_quiz_state(full=True)
            reset_proctor_state()
            st.switch_page("pages/01_home.py")
    st.stop()


# =============================================================
# 3. GENERATE QUESTIONS
# =============================================================

selected_skills = st.session_state["selected_skills"]
student_name    = st.session_state["student_name"]

if not st.session_state.get("_proctor_reset_done"):
    reset_proctor_state()
    st.session_state["_proctor_reset_done"] = True
    st.session_state["quiz_started"] = False

quiz_data = ensure_quiz_data(selected_skills)
if not quiz_data:
    st.error("Failed to generate quiz questions. Please go back and try again.")
    if st.button("Go Back"):
        st.switch_page("pages/02_skill_input.py")
    st.stop()


# =============================================================
# 4. PRE-START GATE
#    Until the student clicks the big green "Start Proctored Test"
#    button, we do not render the camera or the form. Clicking the
#    button (a) requests fullscreen via JS in the parent context,
#    (b) flips quiz_started=True so the rest of the page renders.
#
#    This is the cleanest way to satisfy the browser's user-gesture
#    requirement for fullscreen — the click that starts the test
#    IS the gesture that grants fullscreen.
# =============================================================

quiz_started = st.session_state.get("quiz_started", False)

if not quiz_started:
    st.markdown(
        f"""
        <div class="q-header">
          <div>
            <div class="title">SKILLDRIFT PROCTORED ASSESSMENT</div>
            <div class="sub">
              Candidate: {student_name} &nbsp;·&nbsp;
              Skills: {len(quiz_data)} &nbsp;·&nbsp;
              Total questions: {sum(len(x['questions']) for x in quiz_data)}
            </div>
          </div>
          <div class="vio-badge">Ready to start</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="lock-overlay">
          <div class="title">Proctored Test — Read Before Starting</div>
          <div class="body">
            <div style="margin-bottom:14px;">
              When you click <b>Start Proctored Test</b> below the page
              will enter fullscreen and the camera will activate.
              Please ensure:
            </div>
            <div class="step">Camera permission allowed</div>
            <div class="step">Face clearly visible</div>
            <div class="step">No other tabs open</div>
            <div class="step">Phone away</div>
            <div style="margin-top:18px;font-size:0.85rem;opacity:0.85;">
              Violations: face missing &gt; 8 seconds, tab/window switch, or
              exiting fullscreen. Three violations = automatic termination.
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown('<div class="start-test-btn">', unsafe_allow_html=True)
        start_clicked = st.button(
            "Start Proctored Test",
            type="primary",
            use_container_width=True,
            key="start_proctored_test",
        )
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        cancel_clicked = st.button(
            "Cancel and Go Back",
            use_container_width=True,
            key="pre_cancel",
        )

    if cancel_clicked:
        reset_quiz_state(full=False)
        reset_proctor_state()
        st.switch_page("pages/01_home.py")

    if start_clicked:
        st.session_state["quiz_started"] = True
        # Trigger fullscreen on the parent document. This runs as part of
        # the same user gesture (the button click) so the browser allows it.
        if HAS_JS_EVAL:
            streamlit_js_eval(
                js_expressions=(
                    "(function(){"
                    "  var d = window.parent.document.documentElement;"
                    "  if (d.requestFullscreen) { d.requestFullscreen(); }"
                    "  else if (d.webkitRequestFullscreen) { d.webkitRequestFullscreen(); }"
                    "  else if (d.msRequestFullscreen) { d.msRequestFullscreen(); }"
                    "  return 1;"
                    "})()"
                ),
                key="enter_fs",
            )
        st.rerun()

    st.stop()


# =============================================================
# 5. QUIZ STARTED — set up monitoring bridges
# =============================================================

# Auto-refresh so violation polling actually flows from camera thread
if HAS_AUTOREFRESH:
    st_autorefresh(interval=2500, key="quiz_autorefresh")

# Tab-switch counter via streamlit-js-eval. The JS attaches a listener
# to the PARENT document on first call; subsequent calls just read the
# counter from window.top._sdTabSwitches.
if HAS_JS_EVAL:
    js_attach = """
    (function() {
      var w = window.parent;
      if (!w._sdTabListenerAttached) {
        w._sdTabListenerAttached = true;
        w._sdTabSwitches = 0;
        w._sdFsExits    = 0;

        // Tab visibility
        w.document.addEventListener('visibilitychange', function() {
          if (w.document.hidden) {
            w._sdTabSwitches = (w._sdTabSwitches || 0) + 1;
          }
        });
        // Window blur — also a violation
        w.addEventListener('blur', function() {
          w._sdTabSwitches = (w._sdTabSwitches || 0) + 1;
        });
        // Fullscreen exit
        w.document.addEventListener('fullscreenchange', function() {
          if (!w.document.fullscreenElement) {
            w._sdFsExits = (w._sdFsExits || 0) + 1;
          }
        });

        // Block context menu / keyboard shortcuts at the parent level
        w.document.addEventListener('contextmenu', function(e){ e.preventDefault(); }, true);
        w.document.addEventListener('copy',        function(e){ e.preventDefault(); }, true);
        w.document.addEventListener('cut',         function(e){ e.preventDefault(); }, true);
        w.document.addEventListener('paste',       function(e){ e.preventDefault(); }, true);
        w.document.addEventListener('selectstart', function(e){ e.preventDefault(); }, true);
        w.document.addEventListener('dragstart',   function(e){ e.preventDefault(); }, true);
        w.document.addEventListener('keydown', function(e){
          var k = (e.key || '').toLowerCase();
          if ((e.ctrlKey || e.metaKey) && ['c','v','x','a','p','s','u'].indexOf(k) >= 0) {
            e.preventDefault(); e.stopPropagation();
          }
          if (k === 'f12' || (e.ctrlKey && e.shiftKey && ['i','j','c'].indexOf(k) >= 0)) {
            e.preventDefault(); e.stopPropagation();
          }
        }, true);
      }
      return [w._sdTabSwitches || 0, w._sdFsExits || 0];
    })()
    """
    js_result = streamlit_js_eval(
        js_expressions=js_attach,
        key="proctor_js_poll",
        want_output=True,
    )

    # Reconcile JS counters with Python state
    if isinstance(js_result, list) and len(js_result) == 2:
        ts, fx = int(js_result[0] or 0), int(js_result[1] or 0)
        prev_ts = st.session_state.get("_seen_ts", 0)
        prev_fx = st.session_state.get("_seen_fx", 0)
        for _ in range(max(0, ts - prev_ts)):
            add_tab_switch_violation()
        for _ in range(max(0, fx - prev_fx)):
            add_fullscreen_exit_violation()
        st.session_state["_seen_ts"] = ts
        st.session_state["_seen_fx"] = fx
        # refresh snapshot after possible bumps
        snap = get_proctor_snapshot()
        if snap["violations"] >= 3:
            st.session_state["quiz_terminated"] = True
            st.rerun()


# =============================================================
# 6. HEADER (during test)
# =============================================================

violations = snap["violations"]
total_q = sum(len(x['questions']) for x in quiz_data)
vio_class = "vio-badge"
if   violations >= 3: vio_class += " bad"
elif violations >= 1: vio_class += " warn"

st.markdown(
    f"""
    <div class="q-header">
      <div>
        <div class="title">SKILLDRIFT PROCTORED ASSESSMENT</div>
        <div class="sub">
          Candidate: {student_name} &nbsp;·&nbsp;
          Skills: {len(quiz_data)} &nbsp;·&nbsp;
          Questions: {total_q} &nbsp;·&nbsp;
          Tab switches: {snap['tab_switches']} &nbsp;·&nbsp;
          Face misses: {snap['face_misses']} &nbsp;·&nbsp;
          FS exits: {snap['fs_exits']}
        </div>
      </div>
      <div class="{vio_class}">Violations: {violations} / 3</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =============================================================
# 7. CAMERA + STATUS PANEL
# =============================================================

cam_col, status_col = st.columns([1, 1])

with cam_col:
    st.markdown("**Live Camera (Face Detection Active)**")
    ctx = render_proctor_camera()
    st.caption(
        "Click START on the camera widget. Allow camera access. "
        "The questions unlock once the camera is streaming."
    )

cam_running = (
    snap["running"] and snap["last_frame_time"] is not None
    and (time.time() - snap["last_frame_time"]) < 5
)

with status_col:
    st.markdown("**Proctoring Status**")
    face_status = "Detected" if snap["face_present"] else "Not detected"
    face_color  = "#15803d" if snap["face_present"] else "#ba1a1a"
    cam_status  = "Active" if cam_running else "Not started"
    cam_color   = "#15803d" if cam_running else "#9a3412"
    no_face_streak = snap["no_face_streak"]

    st.markdown(
        f"""
        <div style="background:#fff;border:1px solid #e2e8f0;
                    border-radius:10px;padding:14px 18px;">
          <div style="display:flex;justify-content:space-between;
                      padding:6px 0;border-bottom:1px solid #f0f4f8;">
            <span style="color:#515f74;">Camera</span>
            <span style="color:{cam_color};font-weight:700;">{cam_status}</span>
          </div>
          <div style="display:flex;justify-content:space-between;
                      padding:6px 0;border-bottom:1px solid #f0f4f8;">
            <span style="color:#515f74;">Face</span>
            <span style="color:{face_color};font-weight:700;">{face_status}</span>
          </div>
          <div style="display:flex;justify-content:space-between;
                      padding:6px 0;border-bottom:1px solid #f0f4f8;">
            <span style="color:#515f74;">No-face streak</span>
            <span style="color:#171c1f;font-weight:700;">{no_face_streak:.1f}s / 8s</span>
          </div>
          <div style="display:flex;justify-content:space-between;padding:6px 0;">
            <span style="color:#515f74;">Violations</span>
            <span style="color:#171c1f;font-weight:700;">{violations} / 3</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================
# 8. INSTRUCTIONS
# =============================================================

st.markdown(
    """
    <div class="q-instr">
      <b>Rules.</b> Stay in fullscreen. Keep your face clearly visible. Do not
      switch tabs or windows. Right-click, copy, paste, and developer tools
      are disabled. The test terminates after 3 violations.
    </div>
    """,
    unsafe_allow_html=True,
)


# =============================================================
# 9. CAMERA-LOCK OVERLAY + BLURRED FORM
# =============================================================

if not cam_running:
    st.markdown(
        """
        <div class="lock-overlay">
          <div class="title">Camera not streaming yet</div>
          <div class="body">
            Click <b>START</b> on the camera widget above and allow camera
            access. The quiz unlocks automatically within a few seconds.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================
# 10. THE QUIZ FORM
# =============================================================

if not cam_running:
    st.markdown('<div class="questions-blur">', unsafe_allow_html=True)

with st.form("skill_quiz_form", clear_on_submit=False):
    for skill_idx, item in enumerate(quiz_data):
        skill     = item["skill"]
        level     = item["level"]
        questions = item.get("questions", [])
        source    = item.get("source", "gemini")

        badge = ""
        if source == "fallback":
            badge = "<span class='q-fallback-badge'>Self-assessment</span>"

        st.markdown(
            f"""
            <div class="q-card">
              <div class="skill">{skill}{badge}</div>
              <div class="meta">
                Claimed level: <b>{level}</b> &nbsp;·&nbsp;
                {len(questions)} question{'s' if len(questions)!=1 else ''}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not questions:
            st.warning(
                f"No questions could be generated for {skill}. "
                "It will be marked as Unverified."
            )
            continue

        for q_idx, q in enumerate(questions):
            key = f"q_{skill_idx}_{q_idx}"
            display_text = (
                f"Q{q_idx+1}. " + q.get("question", "")
                if cam_running
                else f"Q{q_idx+1}. (locked — start camera to view question)"
            )
            st.markdown(
                f"<div style='font-weight:600;font-size:0.92rem;"
                f"color:#171c1f;margin:14px 0 6px 0;'>"
                f"{display_text}</div>",
                unsafe_allow_html=True,
            )
            options = [
                f"A. {q.get('option_a','')}",
                f"B. {q.get('option_b','')}",
                f"C. {q.get('option_c','')}",
                f"D. {q.get('option_d','')}",
            ] if cam_running else [
                "A. (locked)", "B. (locked)", "C. (locked)", "D. (locked)"
            ]
            st.radio(
                label=f"Question {skill_idx+1}.{q_idx+1}",
                options=options,
                key=key,
                label_visibility="collapsed",
                index=None,
                disabled=not cam_running,
            )

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

    confirm_cancel = st.session_state.get("_confirm_cancel", False)

    col_a, col_b = st.columns([2, 1])
    with col_a:
        submitted = st.form_submit_button(
            "Submit Test and Continue",
            type="primary",
            use_container_width=True,
            disabled=not cam_running,
        )
    with col_b:
        cancel_clicked = st.form_submit_button(
            "Confirm cancel — go to Home" if confirm_cancel else "Cancel and Go Back",
            use_container_width=True,
            type="secondary",
        )

if not cam_running:
    st.markdown('</div>', unsafe_allow_html=True)


# =============================================================
# 11. HANDLE CANCEL — two-step
# =============================================================

if cancel_clicked:
    if st.session_state.get("_confirm_cancel"):
        st.session_state["_confirm_cancel"] = False
        reset_quiz_state(full=False)
        reset_proctor_state()
        if HAS_JS_EVAL:
            streamlit_js_eval(
                js_expressions="(document.exitFullscreen ? document.exitFullscreen() : null)",
                key="exit_fs_cancel",
            )
        st.switch_page("pages/01_home.py")
    else:
        st.session_state["_confirm_cancel"] = True
        st.warning(
            "Are you sure you want to cancel? Your answers will be lost and "
            "all proctoring state will be cleared. Click the button again "
            "to confirm."
        )
        st.stop()


# =============================================================
# 12. HANDLE SUBMIT
# =============================================================

if submitted and cam_running:
    verified = score_all(quiz_data)

    try:
        render_proctor_camera(key="skilldrift-proctor-stop2",
                              desired_playing=False)
    except Exception:
        pass
    reset_proctor_state()

    if HAS_JS_EVAL:
        streamlit_js_eval(
            js_expressions="(document.exitFullscreen ? document.exitFullscreen() : null)",
            key="exit_fs_submit",
        )

    with st.spinner("Running full career analysis..."):
        try:
            drift_score, drift_label, track_counts = calculate_drift_score(verified)
            entropy_score, entropy_label = calculate_entropy(track_counts)
            career_matches = calculate_career_match(verified)
            best_match = career_matches[0] if career_matches else {}
            best_track = best_match.get("track", "Unknown")
            match_pct  = best_match.get("match_pct", 0.0)
            readiness  = calculate_readiness_score(verified, best_track)
            next_skill = get_next_skill(best_match.get("missing_skills", []), best_track)
            urgency    = get_urgency_level(st.session_state.get("semester", 4))
            debt       = calculate_focus_debt(verified, best_track)
            peer       = get_peer_placement_rate(drift_score, best_track)

            st.session_state["drift_score"]     = drift_score
            st.session_state["drift_label"]     = drift_label
            st.session_state["track_counts"]    = track_counts
            st.session_state["entropy_score"]   = entropy_score
            st.session_state["entropy_label"]   = entropy_label
            st.session_state["career_matches"]  = career_matches
            st.session_state["best_track"]      = best_track
            st.session_state["match_pct"]       = match_pct
            st.session_state["readiness_score"] = readiness
            st.session_state["next_skill_info"] = next_skill
            st.session_state["urgency_info"]    = urgency
            st.session_state["focus_debt_info"] = debt
            st.session_state["peer_info"]       = peer
        except Exception as e:
            st.error(f"Analysis error: {e}")
            st.stop()

    st.success("Analysis complete. Opening your dashboard...")
    st.switch_page("pages/03_drift_score.py")