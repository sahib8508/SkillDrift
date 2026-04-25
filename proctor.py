"""Proctoring module for SkillDrift quiz."""

import threading
import time

import av
import cv2
from streamlit_webrtc import webrtc_streamer, WebRtcMode


_LOCK = threading.Lock()
_STATE = {
    "no_face_seconds": 0.0,
    "no_face_streak":  0.0,
    "last_frame_time": None,
    "violations":      0,
    "last_violation_at": 0.0,
    "face_present":    True,
    "running":         False,
    "tab_switches":    0,
    "face_misses":     0,
    "fs_exits":        0,
}

NO_FACE_VIOLATION_SECONDS  = 8.0
VIOLATION_COOLDOWN_SECONDS = 5.0


_FACE_CASCADE = None
def _get_face_cascade():
    global _FACE_CASCADE
    if _FACE_CASCADE is None:
        path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        _FACE_CASCADE = cv2.CascadeClassifier(path)
    return _FACE_CASCADE


def reset_proctor_state():
    with _LOCK:
        for k, v in {
            "no_face_seconds":   0.0,
            "no_face_streak":    0.0,
            "last_frame_time":   None,
            "violations":        0,
            "last_violation_at": 0.0,
            "face_present":      True,
            "running":           False,
            "tab_switches":      0,
            "face_misses":       0,
            "fs_exits":          0,
        }.items():
            _STATE[k] = v


def get_proctor_snapshot() -> dict:
    with _LOCK:
        return dict(_STATE)


def add_tab_switch_violation():
    with _LOCK:
        _STATE["violations"]    += 1
        _STATE["tab_switches"]  += 1
        _STATE["last_violation_at"] = time.time()


def add_fullscreen_exit_violation():
    with _LOCK:
        _STATE["violations"] += 1
        _STATE["fs_exits"]   += 1
        _STATE["last_violation_at"] = time.time()


def _video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    now = time.time()

    cascade = _get_face_cascade()
    gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, (320, 240))
    faces = cascade.detectMultiScale(
        small, scaleFactor=1.2, minNeighbors=4, minSize=(40, 40)
    )
    face_count = len(faces) if faces is not None else 0

    with _LOCK:
        last = _STATE["last_frame_time"]
        dt = (now - last) if last else 0.0
        if dt < 0 or dt > 5:
            dt = 0.0
        _STATE["last_frame_time"] = now
        _STATE["running"] = True

        if face_count > 0:
            _STATE["face_present"] = True
            _STATE["no_face_streak"] = 0.0
        else:
            _STATE["face_present"] = False
            _STATE["no_face_streak"] += dt
            _STATE["no_face_seconds"] += dt
            if (
                _STATE["no_face_streak"] >= NO_FACE_VIOLATION_SECONDS
                and (now - _STATE["last_violation_at"]) >= VIOLATION_COOLDOWN_SECONDS
            ):
                _STATE["violations"]  += 1
                _STATE["face_misses"] += 1
                _STATE["last_violation_at"] = now
                _STATE["no_face_streak"] = 0.0

    if face_count > 0:
        sx = img.shape[1] / 320.0
        sy = img.shape[0] / 240.0
        for (x, y, w, h) in faces:
            x1 = int(x * sx); y1 = int(y * sy)
            x2 = int((x + w) * sx); y2 = int((y + h) * sy)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, "FACE OK", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(img, "NO FACE", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    return av.VideoFrame.from_ndarray(img, format="bgr24")


def render_proctor_camera(key: str = "skilldrift-proctor",
                          desired_playing: bool = None):
    kwargs = dict(
        key=key,
        mode=WebRtcMode.SENDRECV,
        media_stream_constraints={"video": True, "audio": False},
        video_frame_callback=_video_frame_callback,
        async_processing=True,
        rtc_configuration={
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        },
    )
    if desired_playing is not None:
        kwargs["desired_playing_state"] = desired_playing
    return webrtc_streamer(**kwargs)