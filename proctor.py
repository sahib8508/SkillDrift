"""Proctoring module for SkillDrift quiz.

Tracks face presence, tab switches, and fullscreen exits.
Each violation is recorded with a reason and timestamp. The
quiz page polls get_proctor_snapshot() and shows a warning
overlay until the user acknowledges it. The test terminates
after MAX_VIOLATIONS unique violation events.

Camera proctoring is implemented via a browser getUserMedia +
face-api.js component (no streamlit-webrtc / tornado required).
Face detection runs entirely in the browser using the lightweight
TinyFaceDetector model from face-api.js. Results are written to
window.parent._sdFaceState and read back by the JS proctor poll
on every autorefresh cycle.
"""

import threading
import time

import streamlit.components.v1 as components


# =============================================================
# CONFIG
# =============================================================

MAX_VIOLATIONS              = 3
NO_FACE_VIOLATION_SECONDS   = 5.0
VIOLATION_COOLDOWN_SECONDS  = 8.0


# =============================================================
# SHARED STATE  (thread-safe between rerun cycles)
# =============================================================

_LOCK = threading.Lock()

_STATE = {
    "no_face_streak":       0.0,
    "no_face_seconds":      0.0,
    "last_frame_time":      None,
    "violations":           0,
    "last_violation_at":    0.0,
    "face_present":         True,
    "running":              False,
    "tab_switches":         0,
    "face_misses":          0,
    "fs_exits":             0,
    "pending_warning":      "",
    "pending_warning_at":   0.0,
    "violation_log":        [],
}


# =============================================================
# PUBLIC API
# =============================================================

def reset_proctor_state():
    """Wipe all in-memory proctor state."""
    with _LOCK:
        _STATE.update({
            "no_face_streak":       0.0,
            "no_face_seconds":      0.0,
            "last_frame_time":      None,
            "violations":           0,
            "last_violation_at":    0.0,
            "face_present":         True,
            "running":              False,
            "tab_switches":         0,
            "face_misses":          0,
            "fs_exits":             0,
            "pending_warning":      "",
            "pending_warning_at":   0.0,
        })
        _STATE["violation_log"] = []


def get_proctor_snapshot() -> dict:
    """Read-only copy of the current proctor state."""
    with _LOCK:
        snap = dict(_STATE)
        snap["violation_log"] = list(_STATE["violation_log"])
        return snap


def get_max_violations() -> int:
    return MAX_VIOLATIONS


def get_no_face_threshold() -> float:
    return NO_FACE_VIOLATION_SECONDS


def acknowledge_warning():
    """Clear the pending warning and reset the no-face streak."""
    with _LOCK:
        _STATE["pending_warning"]    = ""
        _STATE["pending_warning_at"] = 0.0
        _STATE["no_face_streak"]     = 0.0


def _record_violation(reason: str, counter_key: str):
    """Internal helper — caller must already hold _LOCK."""
    now = time.time()

    if _STATE.get("pending_warning"):
        return

    if (now - _STATE["last_violation_at"]) < VIOLATION_COOLDOWN_SECONDS:
        return

    _STATE["violations"] += 1
    if counter_key in _STATE:
        _STATE[counter_key] += 1
    _STATE["last_violation_at"] = now

    remaining = max(0, MAX_VIOLATIONS - _STATE["violations"])

    if _STATE["violations"] >= MAX_VIOLATIONS:
        msg = (
            f"Violation {_STATE['violations']} of {MAX_VIOLATIONS}: {reason}. "
            f"You have reached the maximum number of violations. "
            f"The test will be terminated."
        )
    else:
        msg = (
            f"Warning {_STATE['violations']} of {MAX_VIOLATIONS}: {reason}. "
            f"You have {remaining} warning{'s' if remaining != 1 else ''} "
            f"remaining before the test is terminated."
        )

    _STATE["pending_warning"]    = msg
    _STATE["pending_warning_at"] = now
    _STATE["violation_log"].append({"reason": reason, "at": now})


def add_tab_switch_violation():
    with _LOCK:
        _record_violation(
            "you switched away from the test tab or window",
            "tab_switches",
        )


def add_fullscreen_exit_violation():
    with _LOCK:
        _record_violation(
            "you exited fullscreen mode",
            "fs_exits",
        )


def update_face_state(running: bool, face_present: bool,
                      no_face_streak: float, no_face_seconds: float):
    """
    Called by the quiz page after reading JS face detection results.
    Updates _STATE and fires a face-miss violation if streak threshold hit.
    """
    now = time.time()
    with _LOCK:
        _STATE["running"]         = running
        _STATE["face_present"]    = face_present
        _STATE["no_face_seconds"] = no_face_seconds
        _STATE["no_face_streak"]  = no_face_streak
        if running:
            _STATE["last_frame_time"] = now

        if (
            not face_present
            and running
            and no_face_streak >= NO_FACE_VIOLATION_SECONDS
            and not _STATE.get("pending_warning")
            and (now - _STATE["last_violation_at"]) >= VIOLATION_COOLDOWN_SECONDS
        ):
            _record_violation(
                f"your face was not detected for over "
                f"{int(NO_FACE_VIOLATION_SECONDS)} seconds",
                "face_misses",
            )


# =============================================================
# CAMERA WIDGET  (getUserMedia + face-api.js, no WebRTC package)
# =============================================================

_FACE_API_CDN = "https://cdn.jsdelivr.net/npm/face-api.js@0.22.2/dist/face-api.min.js"
_MODEL_BASE   = "https://cdn.jsdelivr.net/npm/@vladmandic/face-api@1.7.13/model"


def render_proctor_camera(key: str = "skilldrift-proctor"):
    """
    Render a camera proctoring widget using browser getUserMedia API.

    The widget:
      1. Requests camera access via navigator.mediaDevices.getUserMedia
      2. Streams video to a hidden <video> element
      3. Samples a frame every 500ms via <canvas> + face-api.js TinyFaceDetector
      4. Writes {running, face_present, no_face_streak, no_face_seconds}
         to window.parent._sdFaceState so the JS proctor poll can read it
    """
    camera_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:transparent; overflow:hidden; }}
#cam-wrap {{
  position: relative;
  width: 100%;
  background: #0d1117;
  border-radius: 8px;
  overflow: hidden;
  min-height: 160px;
}}
video {{
  width: 100%;
  height: auto;
  display: block;
  transform: scaleX(-1);
}}
canvas {{ display: none; }}
#cam-overlay {{
  position: absolute;
  top: 6px; left: 6px;
  background: rgba(0,0,0,0.55);
  color: #fff;
  font-family: monospace;
  font-size: 11px;
  padding: 3px 7px;
  border-radius: 4px;
  pointer-events: none;
}}
#cam-err {{
  color: #f87171;
  font-family: monospace;
  font-size: 12px;
  padding: 14px;
  text-align: center;
  background: #1c0a0a;
  border-radius: 8px;
  display: none;
}}
</style>
</head>
<body>
<div id="cam-wrap">
  <video id="vid" autoplay playsinline muted></video>
  <canvas id="cnv"></canvas>
  <div id="cam-overlay">Loading...</div>
</div>
<div id="cam-err"></div>
<script src="{_FACE_API_CDN}"></script>
<script>
(async function() {{
  var overlay = document.getElementById('cam-overlay');
  var errDiv  = document.getElementById('cam-err');
  var vid     = document.getElementById('vid');
  var cnv     = document.getElementById('cnv');
  var ctx     = cnv.getContext('2d');
  var NO_FACE_THRESH = {NO_FACE_VIOLATION_SECONDS};

  var faceState = {{
    running: false,
    face_present: false,
    no_face_streak: 0.0,
    no_face_seconds: 0.0
  }};

  function writeState() {{
    try {{ window.parent._sdFaceState = Object.assign({{}}, faceState); }} catch(e) {{}}
  }}
  writeState();

  // Load tiny face detector model
  var modelLoaded = false;
  try {{
    await faceapi.nets.tinyFaceDetector.loadFromUri('{_MODEL_BASE}');
    modelLoaded = true;
    overlay.textContent = 'Starting camera...';
  }} catch(e) {{
    overlay.textContent = 'Detector unavailable';
    // Can't load model — mark running & face present (benefit of doubt)
    faceState.running = true;
    faceState.face_present = true;
    writeState();
  }}

  // Start camera stream
  var stream = null;
  try {{
    stream = await navigator.mediaDevices.getUserMedia({{
      video: {{ width: 320, height: 240, facingMode: 'user' }},
      audio: false
    }});
    vid.srcObject = stream;
    await new Promise(function(res) {{ vid.onloadedmetadata = res; }});
    vid.play();
    faceState.running = true;
    overlay.textContent = modelLoaded ? 'Detecting...' : 'Camera active';
    writeState();
  }} catch(e) {{
    document.getElementById('cam-wrap').style.display = 'none';
    errDiv.style.display = 'block';
    errDiv.textContent = 'Camera access denied. Face proctoring disabled.';
    faceState.running = false;
    faceState.face_present = true; // Don't penalise for denied camera
    writeState();
    return;
  }}

  // Detection loop
  var streakStart = null;

  async function detect() {{
    if (!vid.videoWidth) {{ setTimeout(detect, 500); return; }}
    cnv.width  = vid.videoWidth;
    cnv.height = vid.videoHeight;
    ctx.drawImage(vid, 0, 0);

    var now = Date.now() / 1000;
    var faceDetected = false;

    if (modelLoaded) {{
      try {{
        var opts = new faceapi.TinyFaceDetectorOptions({{
          inputSize: 160,
          scoreThreshold: 0.4
        }});
        var result = await faceapi.detectSingleFace(cnv, opts);
        faceDetected = !!result;
      }} catch(e) {{
        faceDetected = true; // Benefit of doubt on error
      }}
    }} else {{
      faceDetected = true;
    }}

    faceState.face_present = faceDetected;

    if (!faceDetected) {{
      if (streakStart === null) streakStart = now;
      var streak = now - streakStart;
      faceState.no_face_streak  = parseFloat(streak.toFixed(1));
      faceState.no_face_seconds = parseFloat(
        (faceState.no_face_seconds + 0.5).toFixed(1)
      );
      overlay.textContent = 'NO FACE \u2014 ' + streak.toFixed(0) + 's';
      overlay.style.background = 'rgba(180,0,0,0.75)';
    }} else {{
      streakStart = null;
      faceState.no_face_streak = 0.0;
      overlay.textContent = '\u25CF FACE OK';
      overlay.style.background = 'rgba(0,120,50,0.75)';
    }}

    writeState();
    setTimeout(detect, 500);
  }}

  setTimeout(detect, 1000);
}})();
</script>
</body>
</html>"""
    try:
        components.html(camera_html, height=200)
    except Exception:
        pass