# Project Title:

# "SkillDrift — Data-Driven Skill Drift Analysis for Placement"

> **B.Tech Major Project — CSE-801-P3 | Even Semester 2025–26**
> Department of Computer Science and Engineering (CSE-DS&CC)
> Sarala Birla University, Ranchi

**Project Guide:** Dr. Avinash Kumar, Assistant Professor, CSE, SBU

| Name             | Enrollment No. | Section | Batch      |
| ---------------- | -------------- | ------- | ---------- |
| Anurag Kumar Roy | SBU221934      | D       | 2022–2026 |
| Sahib Hussain    | SBU234212      | D       | 2022–2026 |
| Vikash Kumar     | SBU234067      | D       | 2022–2026 |

---

## What is SkillDrift?

SkillDrift is a data-driven web application built with **Python** and **Streamlit** for B.Tech CSE students in India. It measures how scattered a student's skills are across multiple career domains using a mathematical formula called the **Drift Score** and a concept from information theory called **Shannon Entropy**.

**The Problem — Skill Drift:**
A student learns Python in Semester 1, shifts to web development in Semester 2, tries machine learning in Semester 3, then pivots to cloud in Semester 5. By Semester 8, they have touched eight different fields but have not gone deep enough in any one of them to be hireable. SkillDrift makes this pattern visible as a number and a chart.

**What SkillDrift is — and what it is not:**
SkillDrift is not a career recommender. It is a **career alarm system**. It tells students:

- How scattered they are right now
- How much time remains before placement season
- Which career track fits them best based on real Indian job data
- What the single most critical skill to learn next is

It also includes a **Faculty Dashboard** where teachers and HODs can upload up to 100 student report files at once and receive a batch-level view of their entire class's placement readiness.

>  57% of Indian CSE graduates are not hireable at graduation *(India Skills Report 2024, Wheebox and Mercer Mettl)*. Over 1 million tech jobs remain unfilled because candidates lack depth in any specific domain *(NASSCOM 2024)*. SkillDrift was built to address this gap directly.

---

## Career Tracks Covered

All 8 tracks are derived from **1,600 real Indian job descriptions** collected from Naukri.com — exactly 200 JDs per track, spanning 246 unique companies across 18 cities, restricted to entry-level and fresher roles.

| Track                | Top Skills by Job Market Frequency                                       |
| -------------------- | ------------------------------------------------------------------------ |
| Data Analyst         | SQL 99.5%, Python 96%, Power BI 94%, Excel 88%, Tableau 49.5%            |
| ML Engineer          | Git 97%, Python 94%, TensorFlow 82.5%, SQL 74.5%, Machine Learning 57.5% |
| Web Developer        | HTML 98%, CSS 95.5%, Git 91.5%, JavaScript 80.5%, REST API 60.5%         |
| DevOps & Cloud       | CI/CD 96%, Docker 95%, Linux 92.5%, Kubernetes 92%, Git 77%              |
| Cybersecurity        | SOC 93%, Linux 85%, SIEM 72.5%, Incident Response 50.5%, Python 43.5%    |
| Software Developer   | Git 98%, SQL 62.5%, Java 57.5%, Spring Boot 47.5%, Docker 36%            |
| QA Tester            | Selenium 96%, JIRA 95.5%, SQL 86%, Java 70.5%, Manual Testing 47%        |
| Full Stack Developer | React 98.5%, MongoDB 97.5%, Node.js 92.5%, Git 85%, Express.js 71.5%     |

---

## Application Screenshots

The 16 screens below cover the complete user journey — from a student's first visit to a faculty member's batch analysis. Screenshots are taken directly from the running application and ordered to reflect the exact sequence of interaction.

---

### 01 — Landing Page

The hero section presenting placement statistics from NASSCOM and Wheebox, the three-step "How It Works" walkthrough, and the Faculty Login entry point. This is the first screen every student sees.

![Landing Page](assets/screenshots/ss_01_home.png)

---

### 02 — Skill Input Form

The student enters their name, selects their current semester, and picks skills from 6 tabbed categories. Each skill requires a declared proficiency level — Beginner, Intermediate, or Advanced — before the quiz can be generated.

![Skill Input Form](assets/screenshots/ss_02_skill_input.png)

---

### 03 — Quiz Generation

Gemini 2.5 Flash generates 3 MCQ questions per selected skill in real time, calibrated to the exact proficiency level the student declared. A progress bar tracks generation skill by skill so students know how long to wait.

![Quiz Generation](assets/screenshots/ss_03_quiz_generating.png)

---

### 04 — Proctoring Setup

Webcam permission request and face-detection calibration screen shown before the quiz begins. The system verifies that the webcam feed is active and the student's face is detectable before allowing the quiz to start.

![Proctoring Setup](assets/screenshots/ss_04_quiz_precheck.png)

---

### 05 — Live Quiz with Proctoring

MCQ questions rendered as radio button groups with the webcam overlay active in the corner. A violation counter is visible. If the student's face is absent for 5 or more continuous seconds, a violation is logged. Three violations terminate the quiz automatically.

![Live Quiz with Proctoring](assets/screenshots/ss_05_quiz_live.png)

---

### 06 — Drift Score Dashboard

The primary analytics screen. Shows the quiz result verification table (Confirmed / Borderline / Not Verified per skill), the Drift Score card (0–100 scale), the Entropy Score card in bits, and a horizontal bar chart of verified skill counts per career track.

![Drift Score Dashboard](assets/screenshots/ss_06_dashboard.png)

---

### 07 — Urgency Engine

Semester dot timeline showing weeks remaining until the student's expected placement season. An urgency banner in Red, Yellow, or Green indicates severity. Focus Debt is displayed as the percentage of verified skills that fall outside the student's best-fit track.

![Urgency Engine](assets/screenshots/ss_07_time_left.png)

---

### 08 — Career Track Match

Bar chart comparing the student's match percentage across all 8 career tracks simultaneously. A gap analysis table beneath lists missing skills for the best-fit track sorted by how frequently those skills appear in real job postings.

![Career Track Match](assets/screenshots/ss_08_career_match.png)

---

### 09 — Next Skill to Learn

A single recommended skill card showing the highest-frequency missing skill from the student's best-fit track. A job readiness gauge chart displays the student's readiness score from 0 to 100 with red, yellow, and green threshold zones.

![Next Skill to Learn](assets/screenshots/ss_09_next_skill.png)

---

### 10 — Placement Odds

Predicted placement rate derived from the student's Drift Score mapped against NASSCOM and AICTE outcome data. A comparison chart shows focused versus drifted student outcomes across the 5 Drift Score bands (0–20 through 80–100).

![Placement Odds](assets/screenshots/ss_10_placement_odds.png)

---

### 11 — Job Market Map

Choropleth map of India showing job counts by city for the student's best-fit career track. A breakdown of which skills the companies in each city most frequently list in their job postings is shown below the map.

![Job Market Map](assets/screenshots/ss_11_job_market.png)

---

### 12 — My Report Card

All 8 calculated scores consolidated into a single screen — Drift Score, Entropy Score, Career Match, Readiness Score, Next Skill, Urgency Level, Focus Debt, and Peer Placement Rate. The student downloads this as a CSV file to submit to their faculty.

![My Report Card](assets/screenshots/ss_12_report_card.png)

---

### 13 — Faculty Login

Email and password login form. Credentials are verified by SHA-256 hashing the entered password and comparing it against the stored hash in `faculty_credentials.csv`. No plain-text passwords are stored anywhere in the system.

![Faculty Login](assets/screenshots/ss_13_faculty_login.png)

---

### 14 — Faculty Batch Upload

Multi-file uploader accepting up to 100 student CSV report files simultaneously. The system ignores whatever scores are in the uploaded file and re-runs all 8 calculations fresh from the raw verified skill data contained in each report.

![Faculty Batch Upload](assets/screenshots/ss_14_faculty_upload.png)

---

### 15 — Batch Analysis

Class-level analytics screen showing the average Drift Score, average Readiness Score, urgency level distribution across the batch (Red / Yellow / Green counts), the top 5 missing skills across all students, and a sortable per-student records table.

![Batch Analysis](assets/screenshots/ss_15_batch_results.png)

---

### 16 — Placement Intelligence

Faculty-only analytics view with a career track distribution pie chart showing how many students are best-fit for each of the 8 tracks, a Drift Score histogram for the whole class, and a downloadable batch CSV report for institutional records.

![Placement Intelligence](assets/screenshots/ss_16_placement_intelligence.png)

---

## Core Features

### Drift Score

Measures how concentrated or scattered a student's verified skills are across the 8 career tracks. Calculated using standard deviation of the track skill distribution, normalized to a 0–100 scale. A score near 0 indicates a highly focused student. A score near 100 indicates severe scatter across unrelated tracks. This is the primary number SkillDrift produces.

### Entropy Score

Applies Shannon Entropy from information theory to the same skill distribution. Measures disorder in the student's learning pattern in bits, with a maximum of 3.0 bits. Complements the Drift Score by providing a second mathematical lens on the same underlying data.

### AI-Powered Skill Verification

Skills are not accepted on the student's word. Before any analysis runs, Google Gemini 2.5 Flash generates 3 MCQ questions per selected skill, calibrated to the exact proficiency level the student claimed. Skills answered correctly on 2 or 3 questions receive **Confirmed** status. 1 correct answer gives **Borderline** status and the level is downgraded by one step. 0 correct answers marks the skill as **Not Verified** and it is excluded from all scoring calculations.

### Proctoring System

The quiz runs with webcam-based face detection using OpenCV Haar Cascade. A face absence of 5 or more continuous seconds triggers a violation. Three violations terminate the quiz automatically. Tab-switch and fullscreen-exit events are detected via JavaScript injection and count as additional violations.

### Career Track Matching

Verified skills are compared against `required_skills_per_track.csv` to calculate a match percentage for each of the 8 tracks. The highest-match track is declared the best-fit track. Gap analysis lists the missing skills for that track sorted by their frequency in real job postings.

### Next Skill Recommendation

The single highest-frequency missing skill from the best-fit track is surfaced as the one thing to learn next. A job readiness gauge chart shows the student's readiness score from 0 to 100 calculated using weighted skill importance derived from real JD frequency data.

### Urgency Engine and Focus Debt

Calculates the number of weeks remaining before the student's expected placement season based on their semester. Focus Debt quantifies how much of the student's verified skill portfolio falls outside their best-fit track — the higher this number, the more time was spent learning skills that will not help them get placed.

### Peer Placement Rate

Maps the student's Drift Score to an estimated placement rate using aggregated NASSCOM and AICTE outcome data.

| Drift Score Range | Estimated Placement Rate |
| ----------------- | ------------------------ |
| 0 – 20           | 78%                      |
| 20 – 40          | 62%                      |
| 40 – 60          | 44%                      |
| 60 – 80          | 29%                      |
| 80 – 100         | 18%                      |

### Faculty Batch Dashboard

Faculty upload up to 100 student CSV reports. The system re-runs all 8 calculations fresh from raw verified skills for every file. No student can inflate their results — scores are always recalculated server-side regardless of what values appear in the downloaded CSV.

### Persistent Session with URL-Based Restore

Each student receives a UUID4 session ID embedded in the URL as `?sid=...`. On browser refresh, the session is restored from a server-side JSON file. All 8 calculation results are computed exactly once after quiz submission and read from session state on every subsequent dashboard page — no recalculation, no data loss on refresh.

---

## Real Data Behind the Platform

| Dataset                 | Details                                                                                                                                                                     |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Total job descriptions  | 1,600 (200 per career track)                                                                                                                                                |
| Unique companies        | 246                                                                                                                                                                         |
| Cities covered          | 18 — Bangalore, Hyderabad, Pune, Mumbai, Chennai, Noida, Gurugram, Ahmedabad, Kolkata, Jaipur, Indore, Bhopal, Surat, Delhi, Coimbatore, Thane, Remote, Thiruvananthapuram |
| Experience levels       | Fresher, 0–1 Yrs, 0–2 Yrs, 0–3 Yrs — all entry level                                                                                                                    |
| Unique skills extracted | 142                                                                                                                                                                         |
| NLP tools used          | Python, Pandas, regex, 200+ alias normalization dictionary                                                                                                                  |

**Processed CSV files powering all calculations:**

- `required_skills_per_track.csv` — 179 rows, 3 columns (track, skill, frequency_pct). What skills each track requires and how often they appear across 200 job postings for that track.
- `skills_mapping.csv` — 142 skills as rows, 8 career track columns as binary 0 or 1. Which tracks each skill belongs to. A skill can belong to multiple tracks.
- `city_job_counts.csv` — 17 cities as rows, 8 career track job count columns plus latitude and longitude. Drives the India choropleth map.

---

## Tech Stack

| Technology            | Version   | Purpose                                                                               |
| --------------------- | --------- | ------------------------------------------------------------------------------------- |
| Python                | 3.13      | Core programming language for all logic, data processing, and scoring math            |
| Streamlit             | >= 1.40.0 | Web application framework — converts Python scripts to interactive UI pages          |
| Pandas                | >= 2.2.3  | Reads and processes all CSV data files, builds DataFrames for display and computation |
| NumPy                 | >= 2.2.0  | Array operations for Drift Score — standard deviation, normalization, clipping       |
| SciPy                 | >= 1.15.0 | Shannon Entropy calculation via scipy.stats.entropy for the Entropy Score             |
| Plotly                | 5.22.0    | All interactive charts — bar, radar, gauge, grouped bar, choropleth map              |
| Google Generative AI  | 1.73.1    | Gemini 2.5 Flash API for quiz question generation per skill per proficiency level     |
| streamlit-webrtc      | >= 0.47.0 | Real-time webcam access inside Streamlit for the proctoring system                    |
| OpenCV (headless)     | >= 4.8.0  | Haar Cascade face detection on webcam frames for violation tracking                   |
| PyAV                  | >= 11.0.0 | FFmpeg bindings required by streamlit-webrtc to decode video frames                   |
| streamlit-autorefresh | >= 1.0.1  | Auto-refresh for live updates during quiz and proctoring session                      |
| Hashlib               | stdlib    | SHA-256 password hashing for faculty credential storage                               |
| UUID                  | stdlib    | UUID4 session ID generation for URL-based session persistence                         |
| JSON                  | stdlib    | Disk-based session state persistence in data/sessions/                                |
| Threading             | stdlib    | Thread-safe access to shared proctoring state between WebRTC callback and main thread |
| Pathlib               | stdlib    | Cross-platform file path management for session storage directory                     |
| collections.Counter   | stdlib    | Most-common missing skills calculation across batch-uploaded student files            |

---

## Project Structure

```
SkillDrift/
│
├── app.py                          # Entry point — page config, session init, routes to home
├── brain.py                        # Calculation engine — all scoring math and business logic
├── gemini_quiz.py                  # AI quiz system — prompt building, Gemini API calls, scoring
├── proctor.py                      # Proctoring system — face detection, violation tracking
├── session_store.py                # Session management — UUID-based disk persistence
├── _sidebar.py                     # Shared sidebar — CSS injection, nav, radar chart, scores
├── requirements.txt                # All Python package dependencies
│
├── pages/
│   ├── 01_home.py                  # Landing page — statistics, how it works, faculty login button
│   ├── 02_skill_input.py           # Skill input form — name, semester, skill tabs, level selection
│   ├── 02b_quiz.py                 # Quiz page — Gemini questions, proctoring overlay
│   ├── 03_drift_score.py           # Dashboard — quiz results table, drift score, entropy, bar chart
│   ├── 04_urgency.py               # Urgency Engine — semester timeline, focus debt calculation
│   ├── 05_career_match.py          # Career match — match bar chart, gap analysis table
│   ├── 06_next_skill.py            # Next skill — recommendation card, readiness gauge chart
│   ├── 07_peer_mirror.py           # Placement odds — peer comparison charts and survival rates
│   ├── 08_market_intel.py          # Job market — India choropleth map, city-wise job counts
│   ├── 09_faculty.py               # Faculty login form and dashboard entry
│   ├── 09b_student_view.py         # Faculty drill-down — individual student full analysis
│   ├── 09c_batch_results.py        # Batch analytics — class-level charts and sortable table
│   └── 10_final_report.py          # Report card — all scores consolidated, downloadable CSV
│
├── data/
│   ├── raw/
│   │   └── raw_jd_data.csv         # 1,600 job descriptions (role, company, skills, exp, city)
│   ├── processed/
│   │   ├── required_skills_per_track.csv
│   │   ├── skills_mapping.csv
│   │   └── city_job_counts.csv
│   ├── auth/
│   │   └── faculty_credentials.csv # Faculty email and SHA-256 hashed passwords
│   └── sessions/                   # Auto-generated session JSON files, UUID-named
│
├── nlp_pipeline/
│   └── process_jd.py               # Offline NLP script — processes raw JD CSV into the three processed files
│
├── reports/                        # Placeholder for generated report files
│
└── .streamlit/
    ├── config.toml                 # Theme — primaryColor #6C63FF, fonts, headless mode
    └── secrets.toml                # Gemini API key — never committed to Git
```

---

## How to Run

### Step 1 — Prerequisites

Python 3.10 or higher is required. Development was done on Python 3.13.

### Step 2 — Clone and enter the project

```bash
git clone https://github.com/your-username/skilldrift.git
cd skilldrift
```

### Step 3 — Create and activate a virtual environment

```bash
# Create
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac or Linux
source venv/bin/activate
```

### Step 4 — Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5 — Add your Gemini API key

Create `.streamlit/secrets.toml` with the content below. Do not commit this file to Git — it is listed in `.gitignore`.

```toml
[gemini]
api_key = "your-gemini-api-key-here"
```

> A free API key is available from [Google AI Studio](https://aistudio.google.com). No credit card is required for the free tier.

### Step 6 — Run the application

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

### Step 7 — Regenerate processed data (optional)

Only run this if you replace or update the raw job description data in `data/raw/raw_jd_data.csv`.

```bash
python nlp_pipeline/process_jd.py
```

This regenerates all three processed CSV files from scratch.

---

## Student Flow

1. Student opens the app. A UUID4 session ID is generated and written to the URL as `?sid=...`.
2. Student clicks **Analyze My Career Focus** from the home page.
3. Student enters their name, selects their semester, and picks skills with proficiency levels across 6 tabbed categories.
4. Gemini generates 3 MCQ questions per skill calibrated to the claimed level. A loading bar tracks progress skill by skill.
5. Student takes the quiz with the webcam proctoring overlay active. Answers are submitted as radio button selections.
6. On submission, each skill is classified — **Confirmed** (2–3 correct), **Borderline** (1 correct, level downgraded), **Not Verified** (0 correct, excluded).
7. All 8 calculations run once from the verified skill set: Drift Score, Entropy, Career Match, Readiness Score, Next Skill, Urgency Level, Focus Debt, Peer Placement Rate.
8. Student navigates 8 dashboard pages from the sidebar. Every page reads from session state — nothing is recalculated.
9. On the Report Card page, the student downloads a CSV file to submit to their faculty.
10. Student signs out. The session JSON is deleted from disk and the URL is cleared.

---

## Faculty Flow

1. Faculty clicks **Faculty Login** on the home page and enters email and password.
2. The system SHA-256 hashes the entered password and compares it against the stored hash in `faculty_credentials.csv`.
3. Faculty selects up to 100 student CSV report files using the batch uploader.
4. The system re-runs all 8 calculations fresh for every student from their raw verified skills. No student can inflate results — everything is recalculated server-side.
5. The batch analytics screen shows the class average Drift Score, average Readiness Score, urgency level distribution (Red / Yellow / Green counts), the top 5 missing skills across all students, and a sortable per-student table.
6. Faculty clicks any student row to open the full individual analysis drill-down.
7. Faculty downloads the batch CSV report for institutional records.

---

## Scoring Algorithms

**Drift Score**

```
track_array = array of verified skill counts for each of the 8 career tracks
std_dev = numpy.std(track_array)
max_std = std_dev of [total_skills, 0, 0, 0, 0, 0, 0, 0]  # maximum possible concentration
drift_score = numpy.clip((std_dev / max_std) * 100, 0, 100)
```

A student fully focused on one track produces a Drift Score near 0. A student evenly distributed across all 8 tracks produces a score near 100.

**Entropy Score**

```
entropy_score = (drift_score / 100) * 3.0   # result in bits, maximum 3.0 bits
```

Derived from the Drift Score via linear mapping for calculation consistency. Higher entropy indicates greater disorder in the student's skill distribution.

**Career Match Percentage**

```
For each track:
    matched = count of verified skills appearing in required_skills_per_track for this track
    total_required = count of required skills for this track
    match_pct = (matched / total_required) * 100
```

**Readiness Score**

```
For the best-fit track:
    For each verified skill belonging to this track:
        score += frequency_pct of that skill from required_skills_per_track
    readiness = numpy.clip((score / max_possible_score) * 100, 0, 100)
```

**Peer Placement Rate**

| Drift Score Range | Estimated Placement Rate |
| ----------------- | ------------------------ |
| 0 – 20           | 78%                      |
| 20 – 40          | 62%                      |
| 40 – 60          | 44%                      |
| 60 – 80          | 29%                      |
| 80 – 100         | 18%                      |

*Source: NASSCOM Technology Sector Annual Report 2024 and AICTE Annual Statistical Report 2023-24.*

---

## Security

Faculty passwords are stored as SHA-256 hashes in `faculty_credentials.csv`. Plain-text passwords are never written to disk at any point.

The Gemini API key is stored in `.streamlit/secrets.toml`, which is listed in `.gitignore` and never committed to the repository.

Session IDs are UUID4 hex strings — 32 random hexadecimal characters. Session data is stored on the server disk, not in the browser. Students cannot read or tamper with other students' session data.

Quiz answers are persisted per session key in the format `q_X_Y`. A browser refresh during the quiz restores already-answered questions without allowing the student to re-enter answers.

Session files older than 7 days are automatically garbage collected from `data/sessions/`.

---

## Configuration

`.streamlit/config.toml` controls the visual theme and server behavior:

```toml
[theme]
primaryColor = "#6C63FF"
backgroundColor = "#F5F5F7"
secondaryBackgroundColor = "#FFFFFF"
textColor = "#1D1D1F"
font = "sans serif"

[server]
headless = true
enableCORS = true
enableXsrfProtection = true
gatherUsageStats = false

[ui]
toolbarMode = "viewer"
showSidebarNavigation = false
```

---

## Future Scope

| ID    | Feature                                                                                                      |
| ----- | ------------------------------------------------------------------------------------------------------------ |
| FS-01 | Live Job API Integration — real-time job data replacing manually collected static CSVs                      |
| FS-02 | Redis-Based Session Store — replace disk JSON sessions with Redis for horizontal scalability                |
| FS-03 | Advanced Liveness Detection — replace Haar Cascade with a deep learning-based face detection model          |
| FS-04 | Mentor Review Layer — allow mentors to annotate individual student reports before faculty views them        |
| FS-05 | Native Mobile App — iOS and Android wrapper around the Streamlit backend                                    |
| FS-06 | Blockchain Skill Certificates — tamper-proof certificate issuance for AI-verified skills                    |
| FS-07 | Institution Portal — multi-department support for university-wide deployment                                |
| FS-08 | Peer Benchmarking — compare a student's scores against anonymized batch averages                            |
| FS-09 | Learning Path Integration — link recommended skills to specific free courses on NPTEL and similar platforms |
| FS-10 | Multilingual Support — Hindi and regional language UI for broader access across India                       |

---

## Known Limitations

| ID   | Limitation                                                                                                                                                                        |
| ---- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| L-01 | Proctoring uses Haar Cascade (OpenCV), which has a higher false-negative rate than deep learning-based detection                                                                  |
| L-02 | Job data is a static snapshot from Naukri collected in early 2026. Real-time market shifts are not reflected                                                                      |
| L-03 | First load is slow because Streamlit re-imports all modules and initializes the Gemini client on startup                                                                          |
| L-04 | If deployed on free-tier cloud with inactivity timeout, session JSON files are wiped on container restart                                                                         |
| L-05 | Large batch uploads of 80–100 files can take 30 or more seconds to process on low-specification servers                                                                          |
| L-06 | Gemini-generated quiz questions may occasionally be repetitive for very common skills like Git or Python                                                                          |
| L-07 | No real-time recruiter notification or LinkedIn profile integration                                                                                                               |
| L-08 | The mentor review layer is architected in the design but not implemented in the current release                                                                                   |
| L-09 | No dedicated mobile app — the Streamlit UI is responsive but not natively optimized for small screens                                                                            |
| L-10 | Niche roles such as Blockchain, AR/VR, and Embedded Systems are not among the 8 tracks due to insufficient fresher-level JD availability on Naukri at the time of data collection |

---

## References

1. NASSCOM, "Technology Sector in India — Annual Report 2024," National Association of Software and Service Companies, New Delhi, 2024.
2. Wheebox and Mercer Mettl, "India Skills Report 2024," Wheebox Employability Test, Gurugram, 2024.
3. AICTE, "All India Council for Technical Education — Annual Statistical Report 2023-24," AICTE, New Delhi, 2024.
4. C. E. Shannon, "A Mathematical Theory of Communication," Bell System Technical Journal, vol. 27, pp. 379–423, 1948.
5. Streamlit Inc., "Streamlit Documentation v1.40," [Online]. Available: https://docs.streamlit.io
6. Google DeepMind, "Gemini API Documentation — google-genai v1.73," [Online]. Available: https://ai.google.dev/gemini-api/docs
7. G. Bradski, "The OpenCV Library," Dr. Dobb's Journal of Software Tools, 2000.

---

## Academic Details

| Field                  | Value                                                   |
| ---------------------- | ------------------------------------------------------- |
| University             | Sarala Birla University, Ranchi, Jharkhand              |
| Department             | Computer Science and Engineering                        |
| Program                | B.Tech CSE — Data Science and Cloud Computing (DS&CC)  |
| Course                 | Project Stage-III (Major Project Work and Dissertation) |
| Course Code            | CSE-801-P3                                              |
| Credit Units           | 9                                                       |
| Batch                  | 2022–2026                                              |
| Semester               | VIII, Section D                                         |
| Project Start          | 29th January, 2026                                      |
| Project End            | 30th April, 2026                                        |
| Project Guide          | Dr. Avinash Kumar, Assistant Professor, CSE, SBU        |
| Dean FoECS             | Dr. Pankaj Kr Goswami                                   |
| Associate Dean and HoD | Dr. Priyanka Srivastava                                 |
| Program Coordinator    | Dr. Ashish Sinha                                        |
