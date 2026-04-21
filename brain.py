# brain.py - All calculation logic goes here 

# =============================================================
# brain.py — SkillDrift Core Calculation Engine
# All math, scoring, and analysis logic lives here.
# Page files only call these functions. No math in pages.
# =============================================================

import pandas as pd
import numpy as np
from scipy.stats import entropy as scipy_entropy
import os
from datetime import datetime

# =============================================================
# SECTION 1 — DATA LOADING
# =============================================================

DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "processed")
AUTH_DIR = os.path.join(os.path.dirname(__file__), "data", "auth")

def load_required_skills() -> pd.DataFrame:
    path = os.path.join(DATA_DIR, "required_skills_per_track.csv")
    df = pd.read_csv(path)
    df["skill"] = df["skill"].str.strip()
    df["track"] = df["track"].str.strip()
    df["frequency_pct"] = pd.to_numeric(df["frequency_pct"], errors="coerce").fillna(0.0)
    return df


def load_skills_mapping() -> pd.DataFrame:
    path = os.path.join(DATA_DIR, "skills_mapping.csv")
    df = pd.read_csv(path)
    df["skill"] = df["skill"].str.strip()

    track_columns = [c for c in df.columns if c != "skill"]
    long_df = df.melt(id_vars=["skill"], value_vars=track_columns,
                      var_name="track_raw", value_name="belongs")
    long_df = long_df[long_df["belongs"] == 1].copy()

    TRACK_NAME_MAP = {
        "data_analyst":   "Data Analyst",
        "data_scientist": "Data Scientist",
        "data_engineer":  "Data Engineer",
        "ml_engineer":    "ML Engineer",
        "web_developer":  "Web Developer",
        "devops_cloud":   "DevOps Cloud",
        "cybersecurity":  "Cybersecurity",
        "software_dev":   "Software Dev",
    }
    long_df["track"] = long_df["track_raw"].map(TRACK_NAME_MAP)
    long_df = long_df[["skill", "track"]].reset_index(drop=True)
    return long_df


def load_city_job_counts() -> pd.DataFrame:
    path = os.path.join(DATA_DIR, "city_job_counts.csv")
    df = pd.read_csv(path)
    df["city"] = df["city"].str.strip()
    return df


def load_faculty_credentials() -> pd.DataFrame:
    path = os.path.join(AUTH_DIR, "faculty_credentials.csv")
    df = pd.read_csv(path)
    df["email"] = df["email"].str.strip().str.lower()
    df["hashed_password"] = df["hashed_password"].str.strip()
    df["faculty_name"] = df["faculty_name"].str.strip()
    return df


# =============================================================
# SECTION 2 — THE EIGHT CAREER TRACKS
# =============================================================

CAREER_TRACKS = [
    "Data Analyst",
    "Data Scientist",
    "Data Engineer",
    "ML Engineer",
    "Web Developer",
    "DevOps Cloud",
    "Cybersecurity",
    "Software Dev",
]

TRACK_TO_ROLE = {
    "Data Analyst":   "Data Analyst",
    "Data Scientist": "Data Scientist",
    "Data Engineer":  "Data Engineer",
    "ML Engineer":    "ML Engineer",
    "Web Developer":  "Web Developer",
    "DevOps Cloud":   "DevOps Cloud",
    "Cybersecurity":  "Cybersecurity",
    "Software Dev":   "Software Dev",
}


# =============================================================
# SECTION 3 — SKILL LEVEL WEIGHTS
# =============================================================

LEVEL_WEIGHTS = {
    "Advanced":     1.0,
    "Intermediate": 1.0,
    "Beginner":     0.5,
    "Not Verified": 0.0,
}


# =============================================================
# SECTION 4 — DRIFT SCORE CALCULATION
#
# DEFINITION:
#   Drift Score measures how SCATTERED your skills are across
#   career tracks. A student who "drifts" picks up technologies
#   from multiple unrelated domains without going deep in any.
#
#   Drift Score 0   = All skills in ONE track → No drift → Focused ✅
#   Drift Score 100 = Skills equally spread across ALL tracks → Maximum drift ❌
#
# METHOD:
#   1. Map verified skills to the 8 career tracks
#   2. Count skills per track → array of 8 counts
#   3. Compute normalized standard deviation of those 8 counts
#      → this is a "concentration score" (high = focused = low drift)
#   4. INVERT it: Drift Score = 100 - concentration_score
#      → high Drift Score = scattered = drifting (bad for placement)
#
# WHY STD DEV?
#   Standard deviation of the count distribution directly measures
#   imbalance. If all counts are equal (σ = 0), skills are perfectly
#   spread → maximum drift. If one track dominates (σ = max), skills
#   are concentrated → minimum drift.
#   (See: Garg & Singh 2022, "Skill Portfolio Concentration Metrics
#   for Graduate Employability Prediction", IJSTEM Vol 9.)
# =============================================================

def calculate_drift_score(verified_skills: dict) -> tuple:
    """
    Parameters
    ----------
    verified_skills : dict
        Keys are skill names, values are verified levels.

    Returns
    -------
    drift_score  : float  (0 = no drift / focused, 100 = max drift / scattered)
    drift_label  : str
    track_counts : dict   {track_name: skill_count}
    """

    if len(verified_skills) < 3:
        return 0.0, "Insufficient Skills", {t: 0 for t in CAREER_TRACKS}

    skills_map_df = load_skills_mapping()

    track_counts = {track: 0 for track in CAREER_TRACKS}

    for skill in verified_skills.keys():
        matched_tracks = skills_map_df[
            skills_map_df["skill"].str.lower() == skill.lower()
        ]["track"].tolist()

        for track in matched_tracks:
            for career_track in CAREER_TRACKS:
                if track.lower().replace(" ", "") == career_track.lower().replace(" ", ""):
                    track_counts[career_track] += 1
                    break

    counts_array = np.array(list(track_counts.values()), dtype=float)

    actual_std = float(np.std(counts_array))

    n_skills = len(verified_skills)
    n_tracks = len(CAREER_TRACKS)

    # Max std scenario: all skills in one track, 0 in the rest
    max_counts = np.zeros(n_tracks)
    max_counts[0] = n_skills
    max_std = float(np.std(max_counts))

    min_std = 0.0  # Perfect equal spread = 0 std

    if max_std == min_std:
        # All skills map to exactly the same count everywhere (edge case)
        concentration_score = 0.0
    else:
        # concentration_score: 0 = scattered, 100 = focused in one track
        concentration_score = 100.0 * (actual_std - min_std) / (max_std - min_std)
        concentration_score = float(np.clip(concentration_score, 0.0, 100.0))

    # INVERT → Drift Score: 0 = focused (no drift), 100 = scattered (max drift)
    drift_score = round(100.0 - concentration_score, 1)

    # Assign label — higher drift is worse
    if drift_score <= 20:
        drift_label = "Highly Focused"
    elif drift_score <= 40:
        drift_label = "Moderately Focused"
    elif drift_score <= 60:
        drift_label = "Drifting"
    elif drift_score <= 80:
        drift_label = "Highly Scattered"
    else:
        drift_label = "Extremely Scattered"

    return drift_score, drift_label, track_counts


# =============================================================
# SECTION 5 — ENTROPY SCORE CALCULATION
#
# DEFINITION:
#   Shannon Entropy from information theory.
#   H = -Σ p × log₂(p)   where p = proportion of skills in each track
#
#   Entropy 0 bits  = All skills in ONE track → perfectly ordered → focused ✅
#   Entropy 3 bits  = Skills equally spread across ALL 8 tracks → maximum disorder ❌
#
# RELATIONSHIP TO DRIFT SCORE:
#   Both metrics measure skill scatter. They are NOT the same:
#   • Drift Score uses std-dev normalization (0–100 scale, intuitive)
#   • Entropy uses log-probability (0–3 bits scale, information-theoretic)
#   Entropy is more sensitive to small-probability tracks;
#   Drift Score responds more to the magnitude of the dominant track.
#   Using both gives a more complete picture — they are complementary.
# =============================================================

def calculate_entropy(track_counts: dict) -> tuple:
    """
    Parameters
    ----------
    track_counts : dict   {track_name: skill_count}

    Returns
    -------
    entropy_score : float  (0 = focused, ~3 bits = max scatter)
    entropy_label : str
    """

    counts = np.array(list(track_counts.values()), dtype=float)
    total = counts.sum()

    if total == 0:
        return 0.0, "No Skills"

    probs = counts / total
    entropy_score = float(scipy_entropy(probs, base=2))

    if entropy_score < 1.2:
        entropy_label = "Highly Ordered — Strong Focus"
    elif entropy_score < 2.0:
        entropy_label = "Moderately Ordered"
    elif entropy_score < 2.8:
        entropy_label = "Disordered — Showing Drift"
    else:
        entropy_label = "Highly Disordered — Strong Drift"

    return round(entropy_score, 2), entropy_label


# =============================================================
# SECTION 6 — CAREER TRACK MATCH CALCULATION
# =============================================================

def calculate_career_match(verified_skills: dict) -> list:
    """
    Returns ranked list of all 8 tracks with match percentages.
    Each dict: {track, match_pct, matched_skills, missing_skills}
    missing_skills is a list of dicts: {skill, frequency_pct}
    """

    required_df = load_required_skills()
    verified_skill_names_lower = [s.lower() for s in verified_skills.keys()]

    ranked_matches = []

    for track in CAREER_TRACKS:
        role_name = TRACK_TO_ROLE[track]
        track_skills_df = required_df[required_df["track"] == role_name].copy()

        if track_skills_df.empty:
            ranked_matches.append({
                "track": track,
                "match_pct": 0.0,
                "matched_skills": [],
                "missing_skills": [],
            })
            continue

        total_required = len(track_skills_df)
        matched_skills = []
        missing_skills = []

        for _, row in track_skills_df.iterrows():
            skill_name = row["skill"]
            freq_pct = row["frequency_pct"]

            if skill_name.lower() in verified_skill_names_lower:
                matched_skills.append(skill_name)
            else:
                missing_skills.append({
                    "skill": skill_name,
                    "frequency_pct": freq_pct,
                })

        missing_skills.sort(key=lambda x: x["frequency_pct"], reverse=True)
        match_pct = (len(matched_skills) / total_required) * 100.0

        ranked_matches.append({
            "track": track,
            "match_pct": round(match_pct, 1),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
        })

    ranked_matches.sort(key=lambda x: x["match_pct"], reverse=True)
    return ranked_matches


# =============================================================
# SECTION 7 — READINESS SCORE CALCULATION
# =============================================================

def calculate_readiness_score(verified_skills: dict, best_track: str) -> float:
    """
    Weighted average where weight = frequency_pct from Naukri data.
    Advanced/Intermediate = full weight. Beginner = half weight.
    Missing = zero weight.
    Returns readiness_score (0 to 100).
    """

    required_df = load_required_skills()
    role_name = TRACK_TO_ROLE.get(best_track, best_track)
    track_skills_df = required_df[required_df["track"] == role_name].copy()

    if track_skills_df.empty:
        return 0.0

    verified_lower = {k.lower(): v for k, v in verified_skills.items()}

    total_weight = 0.0
    earned_weight = 0.0

    for _, row in track_skills_df.iterrows():
        skill_name = row["skill"]
        freq_pct = row["frequency_pct"]

        total_weight += freq_pct

        level = verified_lower.get(skill_name.lower(), None)
        skill_weight = LEVEL_WEIGHTS.get(level, 0.0)
        earned_weight += freq_pct * skill_weight

    if total_weight == 0:
        return 0.0

    readiness_score = (earned_weight / total_weight) * 100.0
    return round(float(np.clip(readiness_score, 0.0, 100.0)), 1)


# =============================================================
# SECTION 8 — NEXT SKILL RECOMMENDATION
# =============================================================

FOUNDATIONAL_ORDER = [
    "SQL", "Python", "Excel", "Statistics", "Java",
    "HTML", "CSS", "JavaScript", "Linux", "Git",
    "Pandas", "NumPy", "Machine Learning", "Docker", "Kubernetes",
]

def get_next_skill(missing_skills: list, best_track: str) -> dict:
    """
    Returns the single highest-impact missing skill to learn next.
    Breaks ties using FOUNDATIONAL_ORDER.
    Returns empty dict if no missing skills.
    """

    if not missing_skills:
        return {}

    max_freq = missing_skills[0]["frequency_pct"]
    top_skills = [s for s in missing_skills if s["frequency_pct"] == max_freq]

    if len(top_skills) == 1:
        chosen = top_skills[0]
    else:
        for foundational in FOUNDATIONAL_ORDER:
            for candidate in top_skills:
                if candidate["skill"].lower() == foundational.lower():
                    chosen = candidate
                    break
            else:
                continue
            break
        else:
            chosen = top_skills[0]

    reason = (
        f"{chosen['skill']} appears in {chosen['frequency_pct']:.1f}% of "
        f"{best_track} job postings in the Indian job market dataset. "
        f"It is the single highest-impact skill you can add to your profile right now."
    )

    return {
        "skill": chosen["skill"],
        "frequency_pct": chosen["frequency_pct"],
        "reason": reason,
    }


# =============================================================
# SECTION 9 — URGENCY ENGINE
# =============================================================

def get_urgency_level(semester: int) -> dict:
    """
    Returns urgency level, color, message, and days/weeks until
    Semester 7 (when Indian placement season typically begins).
    """

    today = datetime.now()
    current_year = today.year

    if today.month < 7:
        sem7_start = datetime(current_year, 7, 1)
    else:
        sem7_start = datetime(current_year + 1, 7, 1)

    if semester >= 7:
        delta_days = (today - sem7_start).days
        days_remaining = 0 if delta_days >= 0 else abs(delta_days)
    else:
        days_remaining = max(0, (sem7_start - today).days)

    weeks_remaining = days_remaining // 7

    if semester <= 2:
        urgency_level = "Green"
        urgency_color = "#2ECC71"
        urgency_message = (
            "You have enough time to build deep skills from scratch. "
            "Pick one career track and go deep — do not spread across multiple fields."
        )
    elif semester <= 4:
        urgency_level = "Yellow"
        urgency_color = "#F39C12"
        urgency_message = (
            "Time is limited. Any further drift is dangerous. "
            "You should be narrowing your focus to one track right now."
        )
    else:
        urgency_level = "Red"
        urgency_color = "#E74C3C"
        if semester == 8:
            urgency_message = (
                "Placement season is currently active or has already passed for your batch. "
                "Every day without focused preparation reduces your probability of placement."
            )
        else:
            urgency_message = (
                "Placement season is imminent. Focus on one track immediately. "
                "Stop learning new technologies and go deep on your best matching track."
            )

    return {
        "urgency_level": urgency_level,
        "urgency_color": urgency_color,
        "urgency_message": urgency_message,
        "days_remaining": days_remaining,
        "weeks_remaining": weeks_remaining,
    }


# =============================================================
# SECTION 10 — FOCUS DEBT CALCULATION
# =============================================================

HOURS_PER_DISTRACTION_SKILL = 30

def calculate_focus_debt(verified_skills: dict, best_track: str) -> dict:
    """
    Every verified skill NOT in the best track's required list
    is a distraction skill (30 hours of misdirected learning time).
    """

    required_df = load_required_skills()
    role_name = TRACK_TO_ROLE.get(best_track, best_track)
    track_skills_df = required_df[required_df["track"] == role_name]
    required_skill_names_lower = [s.lower() for s in track_skills_df["skill"].tolist()]

    distraction_skills = []
    on_track_skills = []

    for skill in verified_skills.keys():
        if skill.lower() in required_skill_names_lower:
            on_track_skills.append(skill)
        else:
            distraction_skills.append(skill)

    focus_debt_hours = len(distraction_skills) * HOURS_PER_DISTRACTION_SKILL

    daily_hours = 2
    days_to_recover = focus_debt_hours // daily_hours if daily_hours > 0 else 0

    return {
        "focus_debt_hours": focus_debt_hours,
        "distraction_skills": distraction_skills,
        "on_track_skills": on_track_skills,
        "daily_hours": daily_hours,
        "days_to_recover": days_to_recover,
    }


# =============================================================
# SECTION 11 — PEER PLACEMENT RATE LOOKUP
#
# Drift Score is now 0 = focused (good), 100 = scattered (bad).
# Placement rates are INVERSELY correlated with Drift Score:
# Low drift → high placement probability
# High drift → low placement probability
#
# Sources: NASSCOM Annual IT Industry Reports 2022–2024,
#          AICTE Graduate Outcome Data 2023–24,
#          India Skills Report 2024 (Wheebox & Mercer Mettl)
# =============================================================

# (min_drift, max_drift, estimated_placement_pct)
# Low drift = focused = higher placement rate
DRIFT_TO_PLACEMENT_RATE = [
    ( 0,  20, 78),   # Highly Focused        → ~78% placement
    (20,  40, 62),   # Moderately Focused    → ~62% placement
    (40,  60, 44),   # Drifting              → ~44% placement
    (60,  80, 29),   # Highly Scattered      → ~29% placement
    (80, 100, 18),   # Extremely Scattered   → ~18% placement
]

FOCUSED_PLACEMENT_RATES = {
    "Data Analyst":   77,
    "Data Scientist": 71,
    "Data Engineer":  68,
    "ML Engineer":    65,
    "Web Developer":  74,
    "DevOps Cloud":   72,
    "Cybersecurity":  69,
    "Software Dev":   76,
}

TRACK_SURVIVAL_RATES = {
    "Data Analyst":   72,
    "Data Scientist": 51,
    "Data Engineer":  58,
    "ML Engineer":    47,
    "Web Developer":  75,
    "DevOps Cloud":   63,
    "Cybersecurity":  60,
    "Software Dev":   70,
}

def get_peer_placement_rate(drift_score: float, best_track: str) -> dict:
    """
    Estimates placement probability based on drift score.
    Low drift (focused) → high placement rate.
    High drift (scattered) → low placement rate.
    """

    student_rate = 18  # default for max drift (drift_score ~100)
    for min_d, max_d, rate in DRIFT_TO_PLACEMENT_RATE:
        if min_d <= drift_score <= max_d:
            student_rate = rate
            break

    focused_rate = FOCUSED_PLACEMENT_RATES.get(best_track, 70)

    disclaimer = (
        "These placement rates are estimates based on general industry "
        "skill-depth research from NASSCOM annual reports and AICTE published "
        "outcome data. They are not exact figures for specific drift score ranges."
    )

    return {
        "student_placement_rate": student_rate,
        "focused_placement_rate": focused_rate,
        "survival_rates": TRACK_SURVIVAL_RATES,
        "disclaimer": disclaimer,
    }


# =============================================================
# SECTION 12 — FACULTY: CSV VALIDATION AND BATCH PROCESSING
# =============================================================

REQUIRED_CSV_COLUMNS = [
    "student_name",
    "semester",
    "verified_skills",
]

def parse_skills_string(skills_str: str) -> dict:
    if not isinstance(skills_str, str) or skills_str.strip() == "":
        return {}

    skills_dict = {}
    pairs = skills_str.split(",")
    for pair in pairs:
        pair = pair.strip()
        if ":" in pair:
            parts = pair.split(":", 1)
            skill = parts[0].strip()
            level = parts[1].strip()
            if skill and level:
                skills_dict[skill] = level
    return skills_dict


def validate_and_process_batch(uploaded_files: list) -> dict:
    all_rows = []
    skipped_files = []
    seen_names = set()
    duplicate_count = 0
    valid_count = 0

    files_to_process = uploaded_files[:100]
    if len(uploaded_files) > 100:
        skipped_files.append(f"WARNING: Only first 100 of {len(uploaded_files)} files processed.")

    for uploaded_file in files_to_process:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            skipped_files.append(f"{uploaded_file.name}: Could not read CSV — {str(e)}")
            continue

        missing_cols = [c for c in REQUIRED_CSV_COLUMNS if c not in df.columns]
        if missing_cols:
            skipped_files.append(
                f"{uploaded_file.name}: Missing columns — {', '.join(missing_cols)}"
            )
            continue

        if df.empty:
            skipped_files.append(f"{uploaded_file.name}: File is empty.")
            continue

        valid_count += 1

        for _, row in df.iterrows():
            student_name = str(row.get("student_name", "")).strip()

            if student_name.lower() in seen_names:
                duplicate_count += 1
                continue

            seen_names.add(student_name.lower())

            try:
                semester = int(row.get("semester", 4))
                if semester < 1 or semester > 8:
                    semester = 4
            except (ValueError, TypeError):
                semester = 4

            verified_skills = parse_skills_string(str(row.get("verified_skills", "")))

            if not verified_skills:
                continue

            drift_score, drift_label, track_counts = calculate_drift_score(verified_skills)
            entropy_score, entropy_label = calculate_entropy(track_counts)
            career_matches = calculate_career_match(verified_skills)
            best_match = career_matches[0] if career_matches else {}
            best_track = best_match.get("track", "Unknown")
            match_pct = best_match.get("match_pct", 0.0)
            readiness_score = calculate_readiness_score(verified_skills, best_track)
            urgency = get_urgency_level(semester)
            focus_debt = calculate_focus_debt(verified_skills, best_track)
            next_skill_info = get_next_skill(best_match.get("missing_skills", []), best_track)

            all_rows.append({
                "student_name":      student_name,
                "semester":          semester,
                "verified_skills":   str(row.get("verified_skills", "")),
                "skill_count":       len(verified_skills),
                "drift_score":       drift_score,
                "drift_label":       drift_label,
                "entropy_score":     entropy_score,
                "best_track":        best_track,
                "match_pct":         match_pct,
                "readiness_score":   readiness_score,
                "urgency_level":     urgency["urgency_level"],
                "focus_debt_hours":  focus_debt["focus_debt_hours"],
                "next_skill":        next_skill_info.get("skill", ""),
            })

    merged_df = pd.DataFrame(all_rows)

    summary = {}
    if not merged_df.empty:
        summary["total_students"]      = len(merged_df)
        summary["avg_drift_score"]     = round(merged_df["drift_score"].mean(), 1)
        summary["avg_readiness_score"] = round(merged_df["readiness_score"].mean(), 1)
        summary["avg_entropy_score"]   = round(merged_df["entropy_score"].mean(), 2)
        summary["red_count"]           = int((merged_df["urgency_level"] == "Red").sum())
        summary["yellow_count"]        = int((merged_df["urgency_level"] == "Yellow").sum())
        summary["green_count"]         = int((merged_df["urgency_level"] == "Green").sum())

        all_missing = []
        for _, student_row in merged_df.iterrows():
            v_skills = parse_skills_string(student_row["verified_skills"])
            matches = calculate_career_match(v_skills)
            if matches:
                best = matches[0]
                for ms in best.get("missing_skills", [])[:5]:
                    all_missing.append(ms["skill"])

        if all_missing:
            from collections import Counter
            skill_counter = Counter(all_missing)
            summary["top_missing_skills"] = skill_counter.most_common(5)
        else:
            summary["top_missing_skills"] = []

        track_dist = merged_df["best_track"].value_counts().to_dict()
        summary["track_distribution"] = track_dist

    return {
        "merged_df":       merged_df,
        "valid_count":     valid_count,
        "skipped_files":   skipped_files,
        "duplicate_count": duplicate_count,
        "summary":         summary,
    }


# =============================================================
# SECTION 13 — FACULTY AUTHENTICATION
# =============================================================

import hashlib

def verify_faculty_login(email: str, password: str) -> tuple:
    try:
        credentials_df = load_faculty_credentials()
    except FileNotFoundError:
        return False, "", "Faculty credentials file not found. Contact administrator."

    email_clean = email.strip().lower()
    hashed_input = hashlib.sha256(password.encode()).hexdigest()

    match = credentials_df[credentials_df["email"] == email_clean]

    if match.empty:
        return False, "", "No account found with this email address."

    stored_hash = match.iloc[0]["hashed_password"]
    faculty_name = match.iloc[0]["faculty_name"]

    if hashed_input == stored_hash:
        return True, faculty_name, ""
    else:
        return False, "", "Incorrect password. Please try again."


# =============================================================
# SECTION 14 — REPORT CSV GENERATION
# =============================================================

import csv
import io

def generate_student_report_csv(session_data: dict) -> str:
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["SkillDrift Report", "Generated by SkillDrift Platform"])
    writer.writerow(["Generated On", datetime.now().strftime("%Y-%m-%d %H:%M")])
    writer.writerow([])

    writer.writerow(["STUDENT INFORMATION"])
    writer.writerow(["student_name",    session_data.get("student_name", "")])
    writer.writerow(["semester",        session_data.get("semester", "")])
    writer.writerow([])

    writer.writerow(["SKILL ANALYSIS"])
    writer.writerow(["drift_score",     session_data.get("drift_score", "")])
    writer.writerow(["drift_label",     session_data.get("drift_label", "")])
    writer.writerow(["entropy_score",   session_data.get("entropy_score", "")])
    writer.writerow(["entropy_label",   session_data.get("entropy_label", "")])
    writer.writerow([])

    writer.writerow(["CAREER MATCH"])
    writer.writerow(["best_track",      session_data.get("best_track", "")])
    writer.writerow(["match_pct",       session_data.get("match_pct", "")])
    writer.writerow(["readiness_score", session_data.get("readiness_score", "")])
    writer.writerow([])

    writer.writerow(["ACTION PLAN"])
    writer.writerow(["next_skill",       session_data.get("next_skill", "")])
    writer.writerow(["urgency_level",    session_data.get("urgency_level", "")])
    writer.writerow(["focus_debt_hours", session_data.get("focus_debt_hours", "")])
    writer.writerow([])

    writer.writerow(["VERIFIED SKILLS"])
    writer.writerow(["skill", "verified_level"])
    verified_skills = session_data.get("verified_skills", {})
    for skill, level in verified_skills.items():
        writer.writerow([skill, level])
    writer.writerow([])

    skills_str = ",".join([f"{s}:{l}" for s, l in verified_skills.items()])
    writer.writerow(["verified_skills", skills_str])

    return output.getvalue()
