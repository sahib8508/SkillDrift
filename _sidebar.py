# _sidebar.py — Shared sidebar renderer used by all dashboard pages
# Import and call render_sidebar() at the top of each dashboard page.

import streamlit as st
import plotly.graph_objects as go

# ── Shared CSS ────────────────────────────────────────────────
APPLE_CSS = """
<style>
    [data-testid="stSidebarNav"] { display: none; }
    .stApp { background-color: #F5F5F7; }
    .block-container { padding-top: 2rem; padding-bottom: 3rem; }

    section[data-testid="stSidebar"] > div {
        background-color: #FFFFFF;
        border-right: 1px solid #D2D2D7;
    }

    h1, h2, h3 { color: #1D1D1F !important; }

    .stButton > button {
        border-radius: 8px;
        border: 1px solid #D2D2D7;
        background: #F5F5F7;
        color: #1D1D1F;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.15s ease;
    }
    .stButton > button:hover { background: #E8E8ED; }
    .stButton > button[kind="primary"] {
        background: #6C63FF;
        color: #FFFFFF;
        border-color: #6C63FF;
    }
    .stButton > button[kind="primary"]:hover { background: #5A52E0; }

    .stProgress > div > div { background-color: #6C63FF; }
    .stAlert { border-radius: 12px; }
    .stMetric {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #D2D2D7;
    }
    div[data-baseweb="tab"] { color: #86868B; }
    div[data-baseweb="tab"][aria-selected="true"] { color: #1D1D1F; }

    /* Dataframe header */
    .stDataFrame thead tr th { background-color: #F5F5F7 !important; color: #1D1D1F !important; }

    /* Score card in sidebar */
    .sd-score-card {
        background: #F5F5F7;
        border: 1px solid #D2D2D7;
        border-radius: 12px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.6rem;
    }
    .sd-score-label {
        color: #86868B;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .sd-score-value {
        font-size: 1.8rem;
        font-weight: 700;
        line-height: 1.2;
    }
    .sd-score-desc {
        color: #86868B;
        font-size: 0.8rem;
        margin-top: 0.15rem;
    }
</style>
"""

NAV_PAGES = [
    ("Drift & Entropy Scores", "pages/03_drift_score.py"),
    ("Urgency Engine",          "pages/04_urgency.py"),
    ("Career Track Match",      "pages/05_career_match.py"),
    ("Next Skill & Readiness",  "pages/06_next_skill.py"),
    ("Peer Mirror",             "pages/07_peer_mirror.py"),
    ("Market Intelligence",     "pages/08_market_intel.py"),
    ("Final Report",            "pages/10_final_report.py"),
]


def render_sidebar():
    """Render the shared dashboard sidebar. Call inside a `with st.sidebar:` block."""
    with st.sidebar:
        # Avatar
        st.markdown("""
        <div style="text-align:center; padding:1.5rem 0 0.75rem 0;">
            <svg width="60" height="60" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
                <circle cx="40" cy="40" r="40" fill="#F0EFFF"/>
                <circle cx="40" cy="30" r="15" fill="#6C63FF"/>
                <ellipse cx="40" cy="65" rx="22" ry="15" fill="#6C63FF"/>
            </svg>
        </div>
        """, unsafe_allow_html=True)

        student_name = st.session_state.get("student_name", "Student")
        st.markdown(
            f"<div style='text-align:center; font-weight:700; font-size:1rem; "
            f"color:#1D1D1F;'>{student_name}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div style='text-align:center; color:#86868B; font-size:0.82rem;'>"
            f"Semester {st.session_state.get('semester', '?')}</div>",
            unsafe_allow_html=True,
        )

        st.markdown("---")

        drift_score   = st.session_state.get("drift_score")
        drift_label   = st.session_state.get("drift_label", "")
        entropy_score = st.session_state.get("entropy_score")
        entropy_label = st.session_state.get("entropy_label", "")

        # Safety: default to 0 if set but None
        drift_score   = drift_score   if drift_score   is not None else None
        entropy_score = entropy_score if entropy_score is not None else 0

        if drift_score is not None:
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

            st.markdown(f"""
            <div class="sd-score-card">
                <div class="sd-score-label">Drift Score</div>
                <div class="sd-score-value" style="color:{drift_color};">{drift_score}</div>
                <div class="sd-score-desc">{drift_label}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="sd-score-card">
                <div class="sd-score-label">Entropy Score</div>
                <div class="sd-score-value" style="color:{entropy_color};">
                    {entropy_score} <span style="font-size:1rem; font-weight:400;">bits</span>
                </div>
                <div class="sd-score-desc">{entropy_label}</div>
            </div>
            """, unsafe_allow_html=True)

            track_counts = st.session_state.get("track_counts") or {}
            if track_counts and any(v > 0 for v in track_counts.values()):
                tracks  = list(track_counts.keys())
                counts  = list(track_counts.values())
                counts_closed = counts + [counts[0]]
                tracks_closed = tracks + [tracks[0]]

                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(
                    r=counts_closed,
                    theta=tracks_closed,
                    fill="toself",
                    fillcolor="rgba(108, 99, 255, 0.15)",
                    line=dict(color="#6C63FF", width=2),
                ))
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, showticklabels=False,
                                        gridcolor="#D2D2D7"),
                        angularaxis=dict(tickfont=dict(size=8, color="#86868B"),
                                         gridcolor="#D2D2D7"),
                        bgcolor="#FFFFFF",
                    ),
                    paper_bgcolor="#FFFFFF",
                    showlegend=False,
                    margin=dict(l=20, r=20, t=15, b=15),
                    height=250,
                )
                st.plotly_chart(fig_radar, use_container_width=True)

        else:
            st.markdown(
                "<div style='color:#86868B; font-size:0.85rem; text-align:center; "
                "padding:0.5rem 0;'>Complete the skill quiz to see your scores.</div>",
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown(
            "<div style='color:#86868B; font-size:0.7rem; font-weight:600; "
            "letter-spacing:1px; padding:0.25rem 0;'>DASHBOARD</div>",
            unsafe_allow_html=True,
        )

        for label, page in NAV_PAGES:
            if st.button(label, key=f"nav_{page}", use_container_width=True):
                st.switch_page(page)

        st.markdown("---")
        if st.button("Sign Out", key="sidebar_signout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.switch_page("pages/01_home.py")
