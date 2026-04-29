# pages/09c_batch_results.py

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import io
from datetime import datetime

st.set_page_config(
    page_title="SkillDrift — Batch Results",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

[data-testid="stSidebarNav"],
[data-testid="collapsedControl"],
[data-testid="stExpandSidebar"],
[data-testid="stSidebarCollapseButton"],
section[data-testid="stSidebar"],
header[data-testid="stHeader"],
.stDeployButton, #MainMenu, footer { display: none !important; }

:root {
    --bg:       #F4F6FB;
    --white:    #FFFFFF;
    --border:   #E1E6F0;
    --border2:  #C8D0E7;
    --ink:      #0D1526;
    --ink2:     #3A4A66;
    --muted:    #7888A8;
    --accent:   #1E40AF;
    --accent-l: #EFF4FF;
    --green:    #0A7B56;
    --green-l:  #E8F8F3;
    --amber:    #A45E00;
    --amber-l:  #FFF7EB;
    --red:      #A8192E;
    --red-l:    #FFF0F2;
    --teal:     #0E7FA8;
    --teal-l:   #EAF7FC;
    --radius:   10px;
    --shadow:   0 1px 4px rgba(13,21,38,0.07), 0 4px 16px rgba(13,21,38,0.04);
}

html, body, .stApp {
    background: var(--bg) !important;
    font-family: 'Outfit', sans-serif !important;
    color: var(--ink) !important;
}
.block-container {
    padding-top: 0 !important;
    padding-bottom: 4rem !important;
    max-width: 1260px !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* ── Top bar ── */
.sd-topbar {
    background: var(--white);
    border-bottom: 1px solid var(--border);
    padding: 1rem 0 0.9rem;
    margin-bottom: 2rem;
}
.sd-topbar-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.sd-wordmark {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 3px;
}
.sd-page-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--ink);
    letter-spacing: -0.025em;
    line-height: 1.2;
}
.sd-meta {
    font-size: 0.7rem;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    margin-top: 3px;
    letter-spacing: 0.04em;
}

/* ── Section labels ── */
.sd-section {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 0.8rem;
    padding-bottom: 0.45rem;
    border-bottom: 1px solid var(--border);
}

/* ── KPI cards ── */
.kpi {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.1rem 1.2rem 1rem;
    box-shadow: var(--shadow);
    position: relative;
    overflow: hidden;
}
.kpi::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 0 0 var(--radius) var(--radius);
}
.kpi.accent::after { background: var(--accent); }
.kpi.green::after  { background: var(--green);  }
.kpi.amber::after  { background: #D97706; }
.kpi.red::after    { background: var(--red);    }
.kpi.teal::after   { background: var(--teal);   }
.kpi.muted::after  { background: var(--border2);}
.kpi-lbl {
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 0.4rem;
}
.kpi-val {
    font-size: 1.9rem;
    font-weight: 800;
    color: var(--ink);
    line-height: 1;
    letter-spacing: -0.02em;
}
.kpi-sub {
    font-size: 0.74rem;
    color: var(--muted);
    margin-top: 0.3rem;
    line-height: 1.4;
}

/* ── Student card ── */
.scard {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.8rem 1rem;
    margin-bottom: 0.35rem;
    box-shadow: var(--shadow);
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.75rem;
}
.scard-name  { font-weight: 700; font-size: 0.9rem; color: var(--ink); }
.scard-sem   { font-size: 0.68rem; color: var(--muted); font-family: 'JetBrains Mono', monospace; }
.scard-lbl   { font-size: 0.58rem; color: var(--muted); font-family: 'JetBrains Mono', monospace; text-transform: uppercase; letter-spacing: 0.09em; }
.scard-val   { font-size: 0.8rem; font-weight: 600; font-family: 'JetBrains Mono', monospace; }

.badge {
    display: inline-block;
    border-radius: 5px;
    padding: 2px 9px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.06em;
}
.badge-red    { background: var(--red-l);   color: var(--red);    border: 1px solid #F5C2C9; }
.badge-amber  { background: var(--amber-l); color: var(--amber);  border: 1px solid #F5D9A8; }
.badge-green  { background: var(--green-l); color: var(--green);  border: 1px solid #A8E5D2; }

/* ── Skill bar ── */
.skill-row {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.65rem 0.9rem;
    margin-bottom: 0.28rem;
    box-shadow: var(--shadow);
}
.skill-row-top {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.3rem;
}
.skill-name { font-weight: 700; font-size: 0.86rem; color: var(--ink); }
.skill-pct  { font-size: 0.72rem; color: var(--muted); font-family: 'JetBrains Mono', monospace; }
.skill-track { height: 3px; background: var(--border); border-radius: 2px; overflow: hidden; }
.skill-fill  { height: 100%; border-radius: 2px; }

/* ── Info banner ── */
.info-banner {
    background: var(--accent-l);
    border: 1px solid #BFCDFF;
    border-radius: var(--radius);
    padding: 0.85rem 1.1rem;
    font-size: 0.85rem;
    color: var(--ink2);
    line-height: 1.65;
    margin-top: 0.65rem;
}
.info-banner strong { color: var(--accent); }

/* ── Matrix description card ── */
.mx-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.25rem;
    box-shadow: var(--shadow);
    height: 100%;
}
.mx-num {
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 0.35rem;
}
.mx-title {
    font-size: 1rem;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 0.6rem;
    letter-spacing: -0.01em;
}
.mx-body {
    font-size: 0.73rem;
    color: var(--ink2);
    line-height: 1.75;
}
.mx-body .g  { color: var(--green); font-weight: 600; }
.mx-body .a  { color: var(--amber); font-weight: 600; }
.mx-body .r  { color: var(--red);   font-weight: 600; }

/* ── Group expander inner ── */
.grp-hdr {
    display: grid;
    grid-template-columns: 3fr 1fr 2fr 2fr 2fr 2fr;
    gap: 0.5rem;
    padding: 0 0.25rem;
    margin-bottom: 0.35rem;
}
.grp-col-lbl {
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
}
.grp-divider { border: none; border-top: 1px solid var(--border); margin: 0.3rem 0 0.55rem; }

/* ── Divider ── */
.sd-divider { border: none; border-top: 1px solid var(--border); margin: 1.75rem 0; }

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 4px !important;
    gap: 3px !important;
    margin-bottom: 1.75rem !important;
    box-shadow: var(--shadow) !important;
}
[data-testid="stTabs"] button[role="tab"] {
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: var(--muted) !important;
    border-radius: 7px !important;
    padding: 0.45rem 1.4rem !important;
    letter-spacing: 0.03em !important;
    transition: all 0.15s !important;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    background: var(--accent) !important;
    color: #FFFFFF !important;
    box-shadow: 0 2px 8px rgba(30,64,175,0.25) !important;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    border-radius: 7px !important;
    border: 1px solid var(--border) !important;
    background: var(--white) !important;
    color: var(--ink2) !important;
    padding: 0.42rem 1rem !important;
    transition: all 0.15s ease !important;
    box-shadow: var(--shadow) !important;
}
.stButton > button:hover {
    background: var(--bg) !important;
    border-color: var(--border2) !important;
    color: var(--ink) !important;
}
.stButton > button[kind="primary"] {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
    color: #FFFFFF !important;
    box-shadow: 0 2px 8px rgba(30,64,175,0.22) !important;
}
.stButton > button[kind="primary"]:hover {
    background: #1636A0 !important;
    border-color: #1636A0 !important;
    box-shadow: 0 4px 14px rgba(30,64,175,0.32) !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow) !important;
}
[data-testid="stExpander"] summary {
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    color: var(--ink) !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# GUARD
# ─────────────────────────────────────────────────────────────────────────────
if not st.session_state.get("faculty_logged_in"):
    st.error("Access denied. Please log in via the Faculty Dashboard.")
    if st.button("Go to Faculty Login"):
        st.switch_page("pages/09_faculty.py")
    st.stop()

results = st.session_state.get("faculty_batch_results")
if not results or not results.get("all_student_analyses"):
    st.warning("No batch data found. Please upload and process student reports first.")
    if st.button("Back to Faculty Dashboard"):
        st.switch_page("pages/09_faculty.py")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# UNPACK
# ─────────────────────────────────────────────────────────────────────────────
all_student_analyses = results["all_student_analyses"]
merged_df            = results.get("merged_df", pd.DataFrame())
valid_count          = results.get("valid_count", 0)
skipped_files        = results.get("skipped_files", [])
duplicate_count      = results.get("duplicate_count", 0)
summary              = results.get("summary", {})
total_students       = summary.get("total_students", len(merged_df))
faculty_name         = st.session_state.get("faculty_name", "Faculty")
today_str            = datetime.now().strftime("%d %b %Y")
files_uploaded       = valid_count + len([s for s in skipped_files if not s.startswith("WARNING")])

student_lookup = {a["student_name"]: a for a in all_student_analyses}
st.session_state["faculty_student_lookup"] = student_lookup

# Classifiers
def classify_drift(s):
    return "fully_focused" if s <= 30 else "moderately_focused" if s <= 60 else "not_focused"
def classify_readiness(s):
    return "high" if s >= 70 else "moderate" if s >= 40 else "poor"
def classify_entropy(s):
    return "highly_ordered" if s < 1.2 else "moderate" if s < 2.2 else "high_disorder"

groups = {
    "drift":     {"fully_focused":[], "moderately_focused":[], "not_focused":[]},
    "readiness": {"high":[], "moderate":[], "poor":[]},
    "entropy":   {"highly_ordered":[], "moderate":[], "high_disorder":[]},
}
for a in all_student_analyses:
    groups["drift"][classify_drift(a["drift_score"])].append(a)
    groups["readiness"][classify_readiness(a["readiness_score"])].append(a)
    groups["entropy"][classify_entropy(a["entropy_score"])].append(a)

# Plotly white base
PW = dict(
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#F4F6FB",
    font=dict(color="#7888A8", family="JetBrains Mono"),
)

# ─────────────────────────────────────────────────────────────────────────────
# TOP BAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="sd-topbar">
    <div class="sd-wordmark">SkillDrift — Faculty Portal</div>
    <div class="sd-page-title">Batch Analysis Results</div>
    <div class="sd-meta">{faculty_name} &nbsp;/&nbsp; {total_students} students &nbsp;/&nbsp; {today_str}</div>
</div>
""", unsafe_allow_html=True)

_, nav_btn = st.columns([11, 1])
with nav_btn:
    if st.button("Back", use_container_width=True):
        st.switch_page("pages/09_faculty.py")

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab_batch, tab_placement = st.tabs(["Batch Analysis", "Placement Intelligence"])


# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 — BATCH ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
with tab_batch:

    # Validation
    st.markdown('<div class="sd-section">Upload Validation</div>', unsafe_allow_html=True)
    v1, v2, v3, v4 = st.columns(4)
    for col, lbl, val, sub, acc in [
        (v1, "Files Uploaded",     files_uploaded,                      "submitted by faculty",         "accent"),
        (v2, "Records Valid",      valid_count,                         "passed validation",            "green"),
        (v3, "Skipped",            max(0, files_uploaded - valid_count),"format or parse errors",       "red"),
        (v4, "Duplicates Removed", duplicate_count,                     "same student, multiple files", "amber"),
    ]:
        with col:
            st.markdown(f'<div class="kpi {acc}"><div class="kpi-lbl">{lbl}</div><div class="kpi-val">{val}</div><div class="kpi-sub">{sub}</div></div>', unsafe_allow_html=True)

    if skipped_files:
        st.markdown("<div style='height:0.6rem;'></div>", unsafe_allow_html=True)
        with st.expander(f"Validation issues — {len(skipped_files)} item(s)"):
            for msg in skipped_files:
                st.markdown(f"<span style='font-family:JetBrains Mono,monospace;font-size:0.78rem;color:var(--red);'>{msg}</span>", unsafe_allow_html=True)

    st.markdown('<hr class="sd-divider">', unsafe_allow_html=True)

    # Batch statistics
    avg_drift     = summary.get("avg_drift_score", 0)
    avg_readiness = summary.get("avg_readiness_score", 0)
    avg_entropy   = summary.get("avg_entropy_score", 0)
    red_count     = summary.get("red_count", 0)
    yellow_count  = summary.get("yellow_count", 0)
    green_count   = summary.get("green_count", 0)

    st.markdown('<div class="sd-section">Batch Statistics</div>', unsafe_allow_html=True)
    m1,m2,m3,m4,m5,m6 = st.columns(6)
    for col, lbl, val, sub, acc in [
        (m1, "Avg Drift",     avg_drift,            "lower = more focused",     "accent"),
        (m2, "Avg Readiness", f"{avg_readiness}%",  "toward best career track", "green"),
        (m3, "Avg Entropy",   f"{avg_entropy} bits","lower = more focused",     "teal"),
        (m4, "High Urgency",  red_count,            "semester 5 and above",     "red"),
        (m5, "Med Urgency",   yellow_count,         "semester 3 to 4",          "amber"),
        (m6, "Low Urgency",   green_count,          "semester 1 to 2",          "muted"),
    ]:
        with col:
            st.markdown(f'<div class="kpi {acc}"><div class="kpi-lbl">{lbl}</div><div class="kpi-val">{val}</div><div class="kpi-sub">{sub}</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1.25rem;'></div>", unsafe_allow_html=True)

    # Charts
    cl, cr = st.columns(2, gap="large")
    with cl:
        st.markdown('<div class="sd-section">Urgency Distribution</div>', unsafe_allow_html=True)
        fig_pie = go.Figure(go.Pie(
            labels=["High Urgency", "Medium Urgency", "Low Urgency"],
            values=[red_count, yellow_count, green_count],
            marker=dict(colors=["#D62B44", "#C27803", "#0A7B56"],
                        line=dict(color="#FFFFFF", width=2)),
            hole=0.58,
            textfont=dict(color="#FFFFFF", size=10, family="JetBrains Mono"),
            hovertemplate="<b>%{label}</b><br>%{value} students<br>%{percent}<extra></extra>",
        ))
        fig_pie.update_layout(**PW, showlegend=True,
            legend=dict(bgcolor="#FFFFFF", font=dict(color="#7888A8", size=10),
                        orientation="h", yanchor="bottom", y=-0.22),
            margin=dict(t=10, b=55, l=10, r=10), height=280)
        st.plotly_chart(fig_pie, use_container_width=True, key="chart_urgency_pie")

    with cr:
        st.markdown('<div class="sd-section">Career Track Distribution</div>', unsafe_allow_html=True)
        track_dist = summary.get("track_distribution", {})
        if track_dist:
            sorted_td = sorted(track_dist.items(), key=lambda x: x[1])
            vals_td   = [v for _, v in sorted_td]
            keys_td   = [k for k, _ in sorted_td]
            fig_track = go.Figure(go.Bar(
                x=vals_td, y=keys_td, orientation="h",
                marker=dict(color=vals_td,
                    colorscale=[[0, "#BFCDFF"], [0.5, "#4B70E0"], [1, "#1E40AF"]],
                    showscale=False,
                    line=dict(color="rgba(0,0,0,0)")),
                text=[str(v) for v in vals_td], textposition="outside",
                textfont=dict(color="#3A4A66", size=10, family="JetBrains Mono"),
            ))
            fig_track.update_layout(**PW,
                xaxis=dict(gridcolor="#E1E6F0", color="#7888A8", zeroline=False),
                yaxis=dict(gridcolor="#E1E6F0", color="#3A4A66", showgrid=False),
                margin=dict(t=10, b=10, l=10, r=50), height=280)
            st.plotly_chart(fig_track, use_container_width=True, key="chart_track_dist")

    st.markdown('<hr class="sd-divider">', unsafe_allow_html=True)

    # Top missing skills
    st.markdown('<div class="sd-section">Skills Most Commonly Missing</div>', unsafe_allow_html=True)
    top_missing = summary.get("top_missing_skills", [])
    if top_missing:
        max_c = top_missing[0][1] if top_missing else 1
        for rank, (skill, count) in enumerate(top_missing, start=1):
            pct  = round((count / total_students) * 100, 1)
            fill = round((count / max_c) * 100)
            fc   = "#D62B44" if rank == 1 else "#C27803" if rank <= 3 else "#1E40AF"
            st.markdown(f"""
            <div class="skill-row">
                <div class="skill-row-top">
                    <span class="skill-name"><span style="color:{fc};font-family:JetBrains Mono,monospace;font-size:0.7rem;">#{rank}</span>&nbsp; {skill}</span>
                    <span class="skill-pct">{count} students &nbsp;·&nbsp; {pct}%</span>
                </div>
                <div class="skill-track">
                    <div class="skill-fill" style="width:{fill}%;background:{fc};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        top_name = top_missing[0][0]
        top_pct  = round((top_missing[0][1] / total_students) * 100, 1)
        st.markdown(f"""
        <div class="info-banner">
            <strong>Faculty Recommendation —</strong>
            {top_pct}% of this batch are missing <strong>{top_name}</strong>.
            A focused workshop before placement season is strongly recommended.
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="sd-divider">', unsafe_allow_html=True)

    # Heatmap
    st.markdown('<div class="sd-section">Skill Coverage Heatmap</div>', unsafe_allow_html=True)
    st.markdown("<span style='font-size:0.7rem;color:#7888A8;font-family:JetBrains Mono,monospace;'>Green = Proficient &nbsp;&nbsp; Amber = Beginner &nbsp;&nbsp; Red = Missing</span>", unsafe_allow_html=True)
    st.markdown("<div style='height:0.4rem;'></div>", unsafe_allow_html=True)

    all_skills_set = set()
    for a in all_student_analyses:
        all_skills_set.update(a["verified_skills"].keys())
    all_skills_list = sorted(list(all_skills_set))

    hmap_data, hmap_labels = [], []
    for a in all_student_analyses:
        hmap_labels.append(a["student_name"][:22])
        row = []
        for sk in all_skills_list:
            lv = a["verified_skills"].get(sk, None)
            row.append(2 if lv in ("Advanced", "Intermediate") else 1 if lv == "Beginner" else 0)
        hmap_data.append(row)

    hmap_matrix = pd.DataFrame(hmap_data, index=hmap_labels, columns=all_skills_list)
    if not hmap_matrix.empty:
        n_s = len(hmap_matrix); n_k = len(all_skills_list)
        fw = max(10, min(n_k * 0.55, 32))
        fh = max(4,  min(n_s * 0.5, 18))
        fig_h, ax = plt.subplots(figsize=(fw, fh))
        fig_h.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FFFFFF")
        cmap = mcolors.ListedColormap(["#FDDDE6", "#FEF3C7", "#D1FAE5"])
        norm = mcolors.BoundaryNorm([-0.5, 0.5, 1.5, 2.5], cmap.N)
        sns.heatmap(hmap_matrix, ax=ax, cmap=cmap, norm=norm,
                    linewidths=0.4, linecolor="#F4F6FB", cbar=True,
                    cbar_kws={"ticks": [0, 1, 2], "label": "Skill Level"})
        cbar = ax.collections[0].colorbar
        cbar.set_ticklabels(["Missing", "Beginner", "Proficient"])
        cbar.ax.yaxis.label.set_color("#7888A8")
        cbar.ax.tick_params(colors="#7888A8", labelsize=8)
        cbar.outline.set_edgecolor("#E1E6F0")
        ax.set_xlabel("Skills", color="#7888A8", fontsize=9, labelpad=8, fontfamily="monospace")
        ax.set_ylabel("Students", color="#7888A8", fontsize=9, labelpad=8, fontfamily="monospace")
        ax.tick_params(colors="#3A4A66", labelsize=7.5)
        ax.set_title(f"Skill Coverage — {n_s} Students × {n_k} Skills",
                     color="#0D1526", fontsize=11, pad=14, fontfamily="monospace", fontweight="bold")
        for spine in ax.spines.values():
            spine.set_edgecolor("#E1E6F0")
        plt.xticks(rotation=45, ha="right", fontsize=7.5, color="#3A4A66")
        plt.yticks(fontsize=8, color="#3A4A66")
        plt.tight_layout()
        st.pyplot(fig_h, use_container_width=True)
        plt.close(fig_h)

    st.markdown('<hr class="sd-divider">', unsafe_allow_html=True)

    # Student cards
    st.markdown('<div class="sd-section">Individual Student Records</div>', unsafe_allow_html=True)
    BADGE_CLS = {"Red": "badge-red", "Yellow": "badge-amber", "Green": "badge-green"}

    for a in all_student_analyses:
        name = a["student_name"]
        bc   = BADGE_CLS.get(a["urgency_level"], "badge-amber")
        rc   = "#0A7B56" if a["readiness_score"] >= 70 else "#A45E00" if a["readiness_score"] >= 40 else "#A8192E"
        dc   = "#0A7B56" if a["drift_score"] <= 30 else "#A45E00" if a["drift_score"] <= 60 else "#A8192E"

        col_card, col_btn = st.columns([11, 1])
        with col_card:
            st.markdown(f"""
            <div class="scard">
                <div style="min-width:150px;">
                    <div class="scard-name">{name}</div>
                    <div class="scard-sem">SEM {a['semester']}</div>
                </div>
                <div style="min-width:130px;">
                    <div class="scard-lbl">Drift Score</div>
                    <div class="scard-val" style="color:{dc};">{a['drift_score']} — {a['drift_label']}</div>
                </div>
                <div style="min-width:140px;">
                    <div class="scard-lbl">Best Track</div>
                    <div class="scard-val" style="color:#1E40AF;">{a['best_track']} ({a['match_pct']}%)</div>
                </div>
                <div style="min-width:95px;">
                    <div class="scard-lbl">Readiness</div>
                    <div class="scard-val" style="color:{rc};">{a['readiness_score']}%</div>
                </div>
                <div style="min-width:85px;">
                    <div class="scard-lbl">Entropy</div>
                    <div class="scard-val" style="color:#0E7FA8;">{a['entropy_score']} bits</div>
                </div>
                <div><span class="badge {bc}">{a['urgency_level'].upper()} URGENCY</span></div>
                <div style="min-width:110px;">
                    <div class="scard-lbl">Next Skill</div>
                    <div class="scard-val" style="color:#A45E00;">{a['next_skill'] or 'N/A'}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_btn:
            if st.button("View", key=f"batch_view_{name}", use_container_width=True):
                st.session_state["faculty_viewing_student"] = name
                st.switch_page("pages/09b_student_view.py")

    st.markdown('<hr class="sd-divider">', unsafe_allow_html=True)

    st.markdown('<div class="sd-section">Export</div>', unsafe_allow_html=True)
    csv_buf = io.StringIO()
    merged_df.to_csv(csv_buf, index=False)
    st.download_button(
        label="Download Full Batch Report (CSV)",
        data=csv_buf.getvalue().encode("utf-8"),
        file_name=f"SkillDrift_Batch_{datetime.now().strftime('%Y_%m_%d')}.csv",
        mime="text/csv", type="primary",
    )
    st.markdown("<span style='font-size:0.72rem;color:#7888A8;font-family:JetBrains Mono,monospace;'>All student records with freshly recalculated scores. Share with placement cell or HOD.</span>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# TAB 2 — PLACEMENT INTELLIGENCE
# ═════════════════════════════════════════════════════════════════════════════
with tab_placement:

    st.markdown(f"""
    <div style="background:#FFFFFF;border:1px solid #E1E6F0;border-radius:10px;
                padding:1.2rem 1.5rem;margin-bottom:1.75rem;
                box-shadow:0 1px 4px rgba(13,21,38,0.06);">
        <div style="font-size:1.1rem;font-weight:700;color:#0D1526;margin-bottom:3px;">
            Placement Intelligence Dashboard
        </div>
        <div style="font-size:0.72rem;color:#7888A8;font-family:'JetBrains Mono',monospace;">
            {total_students} students classified across three independent readiness dimensions.
            Expand any group to inspect individual profiles.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    placement_ready = len(groups["readiness"]["high"])
    fully_focused   = len(groups["drift"]["fully_focused"])
    high_disorder   = len(groups["entropy"]["high_disorder"])
    high_urgency    = sum(1 for a in all_student_analyses if a["urgency_level"] == "Red")

    pk1, pk2, pk3, pk4 = st.columns(4)
    for col, lbl, val, sub, acc in [
        (pk1, "Placement Ready",  placement_ready, f"{round(placement_ready/total_students*100) if total_students else 0}% — readiness 70% or above", "green"),
        (pk2, "Fully Focused",    fully_focused,   f"{round(fully_focused/total_students*100) if total_students else 0}% — drift score 0 to 30",     "teal"),
        (pk3, "Skill Disorder",   high_disorder,   f"{round(high_disorder/total_students*100) if total_students else 0}% — entropy above 2.2 bits",  "red"),
        (pk4, "Urgent Attention", high_urgency,    "semester 5 and above",                                                                            "amber"),
    ]:
        with col:
            st.markdown(f'<div class="kpi {acc}"><div class="kpi-lbl">{lbl}</div><div class="kpi-val">{val}</div><div class="kpi-sub">{sub}</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    # Stacked bar — three-dimension overview
    st.markdown('<div class="sd-section">Three-Dimension Overview</div>', unsafe_allow_html=True)

    drift_v     = [len(groups["drift"]["fully_focused"]),    len(groups["drift"]["moderately_focused"]),    len(groups["drift"]["not_focused"])]
    readiness_v = [len(groups["readiness"]["high"]),         len(groups["readiness"]["moderate"]),          len(groups["readiness"]["poor"])]
    entropy_v   = [len(groups["entropy"]["highly_ordered"]), len(groups["entropy"]["moderate"]),            len(groups["entropy"]["high_disorder"])]

    dims        = [("Skill Drift", drift_v), ("Readiness", readiness_v), ("Entropy", entropy_v)]
    grp_labels  = ["Good", "Moderate", "Needs Attention"]
    grp_colors  = ["#0A7B56", "#C27803", "#A8192E"]

    fig_ov = go.Figure()
    for dim_name, vals in dims:
        total_dim = sum(vals) or 1
        for i, (val, lbl) in enumerate(zip(vals, grp_labels)):
            pct = round(val / total_dim * 100, 1)
            fig_ov.add_trace(go.Bar(
                name=lbl, x=[val], y=[dim_name], orientation="h",
                marker=dict(color=grp_colors[i], line=dict(color="#FFFFFF", width=1.5)),
                text=f"  {val} ({pct}%)" if val > 0 else "",
                textposition="inside",
                textfont=dict(color="#FFFFFF", size=10, family="JetBrains Mono"),
                hovertemplate=f"<b>{lbl}</b><br>{val} students ({pct}%)<extra>{dim_name}</extra>",
                showlegend=(dim_name == "Skill Drift"),
                legendgroup=lbl,
            ))
    fig_ov.update_layout(
        barmode="stack",
        paper_bgcolor="#FFFFFF", plot_bgcolor="#F4F6FB",
        font=dict(color="#7888A8", family="JetBrains Mono"),
        xaxis=dict(title="Number of Students", gridcolor="#E1E6F0", color="#7888A8",
                   title_font=dict(size=10, family="JetBrains Mono")),
        yaxis=dict(color="#0D1526", tickfont=dict(size=12, family="Outfit", color="#0D1526"),
                   categoryorder="array", categoryarray=["Entropy", "Readiness", "Skill Drift"]),
        legend=dict(orientation="h", yanchor="bottom", y=-0.32,
                    bgcolor="rgba(0,0,0,0)", font=dict(color="#3A4A66", size=10, family="JetBrains Mono")),
        margin=dict(t=20, b=75, l=20, r=20), height=280,
    )
    st.plotly_chart(fig_ov, use_container_width=True, key="chart_three_dim_overview")

    st.markdown('<hr class="sd-divider">', unsafe_allow_html=True)

    # Drift vs Readiness scatter
    st.markdown('<div class="sd-section">Drift vs Readiness — Student Map</div>', unsafe_allow_html=True)
    st.markdown("<span style='font-size:0.7rem;color:#7888A8;font-family:JetBrains Mono,monospace;'>Each point is one student. Ideal students cluster bottom-left (low drift, high readiness). Point size = semester.</span>", unsafe_allow_html=True)
    st.markdown("<div style='height:0.4rem;'></div>", unsafe_allow_html=True)

    if all_student_analyses:
        scatter_df = pd.DataFrame([{
            "name": a["student_name"], "drift": a["drift_score"],
            "readiness": a["readiness_score"], "urgency": a["urgency_level"],
            "track": a["best_track"], "semester": a["semester"],
        } for a in all_student_analyses])

        urg_colors = {"Red": "#D62B44", "Yellow": "#C27803", "Green": "#0A7B56"}
        fig_sc = go.Figure()
        for uv, uc in urg_colors.items():
            sub = scatter_df[scatter_df["urgency"] == uv]
            if sub.empty:
                continue
            fig_sc.add_trace(go.Scatter(
                x=sub["drift"], y=sub["readiness"],
                mode="markers+text",
                name=f"{uv} Urgency",
                marker=dict(color=uc, size=sub["semester"] * 3 + 8,
                            opacity=0.85, line=dict(color="#FFFFFF", width=1.5)),
                text=sub["name"],
                textposition="top center",
                textfont=dict(size=8, color="#3A4A66", family="JetBrains Mono"),
                hovertemplate="<b>%{text}</b><br>Drift: %{x}<br>Readiness: %{y}%<extra></extra>",
            ))
        fig_sc.add_shape(type="rect", x0=0, y0=70, x1=30, y1=100,
            fillcolor="rgba(10,123,86,0.06)",
            line=dict(color="rgba(10,123,86,0.25)", width=1, dash="dot"))
        fig_sc.add_annotation(x=15, y=85, text="Ideal Zone", showarrow=False,
            font=dict(color="rgba(10,123,86,0.55)", size=9, family="JetBrains Mono"))
        fig_sc.update_layout(
            paper_bgcolor="#FFFFFF", plot_bgcolor="#F4F6FB",
            font=dict(color="#7888A8", family="JetBrains Mono"),
            xaxis=dict(title="Drift Score  (lower = more focused)", gridcolor="#E1E6F0",
                       color="#7888A8", range=[-5, 105], zeroline=False,
                       title_font=dict(size=10, family="JetBrains Mono")),
            yaxis=dict(title="Readiness  (%)", gridcolor="#E1E6F0",
                       color="#7888A8", range=[-5, 105], zeroline=False,
                       title_font=dict(size=10, family="JetBrains Mono")),
            legend=dict(bgcolor="#FFFFFF", bordercolor="#E1E6F0", borderwidth=1,
                        font=dict(color="#3A4A66", size=10, family="JetBrains Mono")),
            margin=dict(t=20, b=40, l=40, r=20), height=420,
        )
        st.plotly_chart(fig_sc, use_container_width=True, key="chart_scatter_drift_readiness")

    st.markdown('<hr class="sd-divider">', unsafe_allow_html=True)

    # Entropy histogram
    st.markdown('<div class="sd-section">Entropy Distribution</div>', unsafe_allow_html=True)
    if all_student_analyses:
        ent_vals = [a["entropy_score"] for a in all_student_analyses]
        fig_ent = go.Figure()
        fig_ent.add_trace(go.Histogram(
            x=ent_vals,
            nbinsx=min(15, max(5, total_students // 2)),
            marker=dict(
                color=ent_vals,
                colorscale=[[0, "#A8E5D2"], [0.45, "#FDE68A"], [1, "#FECDD3"]],
                line=dict(color="#FFFFFF", width=0.8),
                cmin=0, cmax=3,
            ),
            hovertemplate="Entropy %{x:.2f} bits<br>Count: %{y}<extra></extra>",
        ))
        for thresh, label, color in [
            (1.2, "Focus Threshold",    "#0A7B56"),
            (2.2, "Disorder Threshold", "#A8192E"),
        ]:
            fig_ent.add_vline(x=thresh, line_dash="dash", line_color=color, line_width=1.5,
                annotation=dict(text=label, font=dict(color=color, size=9, family="JetBrains Mono"),
                                yanchor="top"))
        fig_ent.update_layout(
            paper_bgcolor="#FFFFFF", plot_bgcolor="#F4F6FB",
            font=dict(color="#7888A8", family="JetBrains Mono"),
            showlegend=False,
            xaxis=dict(title="Shannon Entropy (bits)", gridcolor="#E1E6F0", color="#7888A8",
                       title_font=dict(size=10, family="JetBrains Mono")),
            yaxis=dict(title="Number of Students", gridcolor="#E1E6F0", color="#7888A8",
                       title_font=dict(size=10, family="JetBrains Mono")),
            margin=dict(t=20, b=40, l=40, r=20), height=280,
        )
        st.plotly_chart(fig_ent, use_container_width=True, key="chart_entropy_hist")

    st.markdown('<hr class="sd-divider">', unsafe_allow_html=True)

    # ── render_group helper ───────────────────────────────────────────────────
    # KEY FIX: every st.plotly_chart inside gets a unique key built from
    # matrix_key + group_key so there are never duplicate element IDs.
    # ─────────────────────────────────────────────────────────────────────────
    def render_group(matrix_key, group_key, label, range_desc, total):
        student_list = groups[matrix_key][group_key]
        count = len(student_list)
        pct   = round((count / total) * 100) if total > 0 else 0

        with st.expander(f"{label}  —  {count} student{'s' if count != 1 else ''}  ({pct}%)  ·  {range_desc}", expanded=False):
            if not student_list:
                st.markdown("<span style='color:#7888A8;font-size:0.82rem;font-family:JetBrains Mono,monospace;'>No students in this group.</span>", unsafe_allow_html=True)
                return

            # Mini readiness bar chart — unique key prevents duplicate element ID
            if len(student_list) >= 2:
                mini_v = [a["readiness_score"] for a in student_list]
                mini_n = [a["student_name"] for a in student_list]
                mini_c = ["#0A7B56" if v >= 70 else "#C27803" if v >= 40 else "#D62B44" for v in mini_v]
                fig_m = go.Figure(go.Bar(
                    x=mini_n, y=mini_v,
                    marker=dict(color=mini_c, line=dict(color="#FFFFFF", width=0.5)),
                    text=[f"{v}%" for v in mini_v],
                    textposition="outside",
                    textfont=dict(color="#3A4A66", size=9, family="JetBrains Mono"),
                    hovertemplate="%{x}<br>Readiness: %{y}%<extra></extra>",
                ))
                fig_m.update_layout(
                    paper_bgcolor="#FFFFFF", plot_bgcolor="#F4F6FB",
                    font=dict(color="#7888A8", family="JetBrains Mono"),
                    xaxis=dict(gridcolor="#E1E6F0", color="#7888A8",
                               tickfont=dict(size=8, family="JetBrains Mono")),
                    yaxis=dict(gridcolor="#E1E6F0", color="#7888A8",
                               range=[0, 115], title="Readiness %",
                               title_font=dict(size=9, family="JetBrains Mono")),
                    showlegend=False,
                    margin=dict(t=10, b=10, l=40, r=10),
                    height=150,
                )
                # UNIQUE KEY = matrix_key + group_key
                st.plotly_chart(fig_m, use_container_width=True,
                                key=f"grp_chart_{matrix_key}_{group_key}")

            # Column headers
            h1,h2,h3,h4,h5,h6 = st.columns([3,1,2,2,2,2])
            for hc, ht in zip([h1,h2,h3,h4,h5,h6],
                              ["Name","Sem","Drift","Readiness","Track","Next Skill"]):
                hc.markdown(f"<span style='font-size:0.58rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#7888A8;font-family:JetBrains Mono,monospace;'>{ht}</span>", unsafe_allow_html=True)

            st.markdown("<hr style='border:none;border-top:1px solid #E1E6F0;margin:0.3rem 0 0.55rem;'>", unsafe_allow_html=True)

            for s in student_list:
                rc2 = "#0A7B56" if s["readiness_score"] >= 70 else "#C27803" if s["readiness_score"] >= 40 else "#D62B44"
                dc2 = "#0A7B56" if s["drift_score"] <= 30 else "#C27803" if s["drift_score"] <= 60 else "#D62B44"

                c1,c2,c3,c4,c5,c6 = st.columns([3,1,2,2,2,2])
                c1.markdown(f"<span style='font-weight:700;font-size:0.87rem;color:#0D1526;'>{s['student_name']}</span>", unsafe_allow_html=True)
                c2.markdown(f"<span style='font-family:JetBrains Mono,monospace;font-size:0.76rem;color:#7888A8;'>{s['semester']}</span>", unsafe_allow_html=True)
                c3.markdown(f"<span style='font-family:JetBrains Mono,monospace;font-size:0.78rem;color:{dc2};font-weight:600;'>{s['drift_score']}</span>", unsafe_allow_html=True)
                c4.markdown(f"<span style='font-family:JetBrains Mono,monospace;font-size:0.78rem;color:{rc2};font-weight:600;'>{s['readiness_score']}%</span>", unsafe_allow_html=True)
                c5.markdown(f"<span style='font-family:JetBrains Mono,monospace;font-size:0.73rem;color:#1E40AF;'>{s['best_track']}</span>", unsafe_allow_html=True)
                c6.markdown(f"<span style='font-family:JetBrains Mono,monospace;font-size:0.73rem;color:#A45E00;'>{s['next_skill'] or 'N/A'}</span>", unsafe_allow_html=True)

                if st.button("View Dashboard",
                             key=f"pl_btn_{matrix_key}_{group_key}_{s['student_name']}"):
                    st.session_state["faculty_viewing_student"] = s["student_name"]
                    st.switch_page("pages/09b_student_view.py")

                st.markdown("<div style='border-top:1px solid #F0F2F8;margin:0.25rem 0;'></div>", unsafe_allow_html=True)

    # ── Matrix 1 — Drift ─────────────────────────────────────────────────────
    mx1l, mx1r = st.columns([3, 5])
    with mx1l:
        st.markdown("""
        <div class="mx-card">
            <div class="mx-num">Matrix 01</div>
            <div class="mx-title">Skill Drift</div>
            <div class="mx-body">
                Measures how scattered skills are across the 8 career tracks.<br><br>
                <span class="g">Fully Focused</span> — drift score 0 to 30<br>
                <span class="a">Moderately Focused</span> — drift 31 to 60<br>
                <span class="r">Not Focused</span> — drift score 61 to 100
            </div>
        </div>
        """, unsafe_allow_html=True)
        dv = [len(groups["drift"]["fully_focused"]),
              len(groups["drift"]["moderately_focused"]),
              len(groups["drift"]["not_focused"])]
        fig_d = go.Figure(go.Pie(
            labels=["Fully Focused", "Moderately Focused", "Not Focused"],
            values=dv,
            marker=dict(colors=["#0A7B56", "#C27803", "#A8192E"],
                        line=dict(color="#FFFFFF", width=2)),
            hole=0.65, textinfo="none",
            hovertemplate="%{label}<br>%{value} students<extra></extra>",
        ))
        fig_d.update_layout(**PW, showlegend=False,
            margin=dict(t=10, b=10, l=10, r=10), height=160)
        st.plotly_chart(fig_d, use_container_width=True, key="mx_donut_drift")

    with mx1r:
        st.markdown('<div class="sd-section">Groups — click to expand</div>', unsafe_allow_html=True)
        render_group("drift", "fully_focused",     "Fully Focused",      "Drift 0 – 30",   total_students)
        render_group("drift", "moderately_focused","Moderately Focused",  "Drift 31 – 60",  total_students)
        render_group("drift", "not_focused",       "Not Focused",         "Drift 61 – 100", total_students)

    st.markdown('<hr class="sd-divider">', unsafe_allow_html=True)

    # ── Matrix 2 — Readiness ─────────────────────────────────────────────────
    mx2l, mx2r = st.columns([3, 5])
    with mx2l:
        st.markdown("""
        <div class="mx-card">
            <div class="mx-num">Matrix 02</div>
            <div class="mx-title">Placement Readiness</div>
            <div class="mx-body">
                Weighted score: verified skills vs. job posting frequency in Indian market data.<br><br>
                <span class="g">High</span> — readiness 70% or above<br>
                <span class="a">Moderate</span> — readiness 40 to 69%<br>
                <span class="r">Poor</span> — readiness below 40%
            </div>
        </div>
        """, unsafe_allow_html=True)
        rv = [len(groups["readiness"]["high"]),
              len(groups["readiness"]["moderate"]),
              len(groups["readiness"]["poor"])]
        fig_r = go.Figure(go.Pie(
            labels=["High", "Moderate", "Poor"],
            values=rv,
            marker=dict(colors=["#0A7B56", "#C27803", "#A8192E"],
                        line=dict(color="#FFFFFF", width=2)),
            hole=0.65, textinfo="none",
            hovertemplate="%{label}<br>%{value} students<extra></extra>",
        ))
        fig_r.update_layout(**PW, showlegend=False,
            margin=dict(t=10, b=10, l=10, r=10), height=160)
        st.plotly_chart(fig_r, use_container_width=True, key="mx_donut_readiness")

    with mx2r:
        st.markdown('<div class="sd-section">Groups — click to expand</div>', unsafe_allow_html=True)
        render_group("readiness", "high",     "High Readiness",     "Readiness 70% or above", total_students)
        render_group("readiness", "moderate", "Moderate Readiness", "Readiness 40 – 69%",     total_students)
        render_group("readiness", "poor",     "Poor Readiness",     "Readiness below 40%",    total_students)

    st.markdown('<hr class="sd-divider">', unsafe_allow_html=True)

    # ── Matrix 3 — Entropy ───────────────────────────────────────────────────
    mx3l, mx3r = st.columns([3, 5])
    with mx3l:
        st.markdown("""
        <div class="mx-card">
            <div class="mx-num">Matrix 03</div>
            <div class="mx-title">Skill Entropy</div>
            <div class="mx-body">
                Shannon Entropy measures disorder in the skill distribution.
                Lower bits means more focused.<br><br>
                <span class="g">Highly Ordered</span> — below 1.2 bits<br>
                <span class="a">Moderate</span> — 1.2 to 2.2 bits<br>
                <span class="r">High Disorder</span> — above 2.2 bits
            </div>
        </div>
        """, unsafe_allow_html=True)
        ev = [len(groups["entropy"]["highly_ordered"]),
              len(groups["entropy"]["moderate"]),
              len(groups["entropy"]["high_disorder"])]
        fig_e = go.Figure(go.Pie(
            labels=["Highly Ordered", "Moderate", "High Disorder"],
            values=ev,
            marker=dict(colors=["#0A7B56", "#C27803", "#A8192E"],
                        line=dict(color="#FFFFFF", width=2)),
            hole=0.65, textinfo="none",
            hovertemplate="%{label}<br>%{value} students<extra></extra>",
        ))
        fig_e.update_layout(**PW, showlegend=False,
            margin=dict(t=10, b=10, l=10, r=10), height=160)
        st.plotly_chart(fig_e, use_container_width=True, key="mx_donut_entropy")

    with mx3r:
        st.markdown('<div class="sd-section">Groups — click to expand</div>', unsafe_allow_html=True)
        render_group("entropy", "highly_ordered", "Highly Ordered", "Entropy below 1.2 bits",  total_students)
        render_group("entropy", "moderate",       "Moderate",       "Entropy 1.2 – 2.2 bits",  total_students)
        render_group("entropy", "high_disorder",  "High Disorder",  "Entropy above 2.2 bits",  total_students)

    st.markdown('<hr class="sd-divider">', unsafe_allow_html=True)

    # Full classification table
    st.markdown('<div class="sd-section">Complete Classification Table</div>', unsafe_allow_html=True)
    DRIFT_LBL    = {"fully_focused": "Fully Focused", "moderately_focused": "Moderately Focused", "not_focused": "Not Focused"}
    READINESS_LBL = {"high": "High", "moderate": "Moderate", "poor": "Poor"}
    ENTROPY_LBL   = {"highly_ordered": "Highly Ordered", "moderate": "Moderate", "high_disorder": "High Disorder"}

    rows = []
    for a in all_student_analyses:
        rows.append({
            "Student":         a["student_name"],
            "Sem":             a["semester"],
            "Drift Score":     a["drift_score"],
            "Drift Group":     DRIFT_LBL[classify_drift(a["drift_score"])],
            "Readiness %":     a["readiness_score"],
            "Readiness Group": READINESS_LBL[classify_readiness(a["readiness_score"])],
            "Entropy (bits)":  a["entropy_score"],
            "Entropy Group":   ENTROPY_LBL[classify_entropy(a["entropy_score"])],
            "Best Track":      a["best_track"],
            "Urgency":         a["urgency_level"],
            "Next Skill":      a["next_skill"],
        })

    summary_df = pd.DataFrame(rows)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    st.markdown("<div style='height:0.75rem;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sd-section">Export for Placement Cell</div>', unsafe_allow_html=True)
    pl_buf = io.StringIO()
    summary_df.to_csv(pl_buf, index=False)
    st.download_button(
        label="Download Placement Classification Report (CSV)",
        data=pl_buf.getvalue().encode("utf-8"),
        file_name=f"SkillDrift_Placement_{datetime.now().strftime('%Y_%m_%d')}.csv",
        mime="text/csv", type="primary",
    )
    st.markdown("<span style='font-size:0.72rem;color:#7888A8;font-family:JetBrains Mono,monospace;'>Drift group, readiness group, entropy group, best track, urgency, and next skill for every student.</span>", unsafe_allow_html=True)