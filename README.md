# SkillDrift: Data-Driven Skill Drift Analysis for Placements

**Department of Computer Science and Engineering (CSE-DS&CC)**
Sarala Birla University, Ranchi | B.Tech Major Project — CSE-801-P3 | Even Sem 2025-26

**Project Guide:** Dr. Avinash Kumar, Assistant Professor, CSE, SBU

**Team Members:**

| Name             | Enrollment No. | Section | Batch     |
| ---------------- | -------------- | ------- | --------- |
| Anurag Kumar Roy | SBU221934      | D       | 2022-2026 |
| Sahib Hussain    | SBU234212      | D       | 2023-2026 |
| Vikash Kumar     | SBU234067      | D       | 2023-2026 |

---

## What is SkillDrift

SkillDrift is a data-driven web application built with Python and Streamlit for B.Tech CSE students in India. It measures how scattered a student's skills are across multiple career domains using a mathematical formula called the **Drift Score** and a concept from information theory called **Shannon Entropy**.

The problem it solves is called **Skill Drift**. A student learns Python in Semester 1, switches to web development in Semester 2, tries machine learning in Semester 3, then cloud in Semester 5. By Semester 8 they have touched eight fields but are not deep enough in any one of them to get a job. SkillDrift makes this pattern visible as a number and a chart.

The platform is not a career recommender. It is a **career alarm system**. It shows students how scattered they are right now, how much time they have before placement season, what their best matching career track is based on real Indian job data, and what the single most important skill to learn next is.

It also includes a **Faculty Dashboard** where teachers and HODs can upload up to 100 student report files at once and get a batch-level view of their entire class's placement readiness.

> 57% of Indian CSE graduates are not hireable at graduation (India Skills Report 2024, Wheebox and Mercer Mettl). Over 1 million tech jobs remain unfilled because candidates lack depth in any specific domain (NASSCOM 2024). SkillDrift was built to address this gap.

---

## Career Tracks Covered

| Track                | Key Skills (Top Frequency from 200 JDs each)                             |
| -------------------- | ------------------------------------------------------------------------ |
| Data Analyst         | SQL 99.5%, Python 96%, Power BI 94%, Excel 88%, Tableau 49.5%            |
| ML Engineer          | Git 97%, Python 94%, TensorFlow 82.5%, SQL 74.5%, Machine Learning 57.5% |
| Web Developer        | HTML 98%, CSS 95.5%, Git 91.5%, JavaScript 80.5%, REST API 60.5%         |
| DevOps & Cloud       | CI/CD 96%, Docker 95%, Linux 92.5%, Kubernetes 92%, Git 77%              |
| Cybersecurity        | SOC 93%, Linux 85%, SIEM 72.5%, Incident Response 50.5%, Python 43.5%    |
| Software Developer   | Git 98%, SQL 62.5%, Java 57.5%, Spring Boot 47.5%, Docker 36%            |
| QA Tester            | Selenium 96%, JIRA 95.5%, SQL 86%, Java 70.5%, Manual Testing 47%        |
| Full Stack Developer | React 98.5%, MongoDB 97.5%, Node.js 92.5%, Git 85%, Express.js 71.5%     |

All 8 tracks are derived from **1,600 real Indian job descriptions** collected from Naukri.com (200 JDs per track, 246 unique companies, 18 cities, all entry-level and fresher roles).

---

## Application Screenshots

The table below shows all 16 screens of SkillDrift in the order a student and faculty member would encounter them.

| #  | Screen                               | Description                                                                                                                |
| -- | ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| 1  | Landing Page (Home)                  | Hero section with placement statistics, How It Works steps, and Faculty Login button                                       |
| 2  | Skill Input Form                     | Student enters name, selects semester, picks skills with Beginner / Intermediate / Advanced level from 6 tabbed categories |
| 3  | Quiz Generation (Loading Screen)     | Gemini AI generates 3 MCQ questions per selected skill in real time with a progress bar                                    |
| 4  | Proctoring Setup Screen              | Webcam permission request and face-detection calibration before quiz begins                                                |
| 5  | Quiz in Session with Proctoring      | MCQ questions rendered with webcam overlay active, violation counter visible                                               |
| 6  | Dashboard — Drift Score and Entropy | Quiz result verification table, Drift Score card, Entropy Score card, horizontal bar chart of skills per track             |
| 7  | Urgency Engine (Time Left)           | Semester dot timeline showing weeks remaining, urgency level banner (Red / Yellow / Green), Focus Debt calculation         |
| 8  | Career Track Match                   | Bar chart comparing match percentage across all 8 tracks, gap analysis table of missing skills                             |
| 9  | Next Skill to Learn                  | Single recommended skill card, job readiness gauge chart with red / yellow / green zones                                   |
| 10 | Placement Odds                       | Predicted placement rate, focused vs drifted student comparison chart, survival rate bars                                  |
| 11 | Job Market Map                       | Choropleth map of India showing job count by city per career track, skills companies want                                  |
| 12 | My Report Card                       | All scores in one view, downloadable CSV report the student saves and submits to faculty                                   |
| 13 | Faculty Login                        | Email and password login form with SHA-256 hashed credential verification                                                  |
| 14 | Faculty Dashboard (Upload)           | Batch file uploader accepting up to 100 student CSV report files at once                                                   |
| 15 | Batch Analysis (Student Records)     | Class average drift score, urgency level counts, top 5 missing skills, per-student sortable table                          |
| 16 | Placement Intelligence (Faculty)     | Track distribution pie chart, drift histogram, downloadable batch CSV report for institutional use                         |

---

## Core Features

**Drift Score**
Measures how concentrated or scattered a student's skills are across the 8 career tracks. Calculated using standard deviation of the track distribution normalized to a 0-100 scale. A score near 0 means highly focused. A score near 100 means severely scattered.

**Entropy Score**
Applies Shannon Entropy from information theory to the same skill distribution. Measures disorder in the student's learning pattern in bits. Complements the Drift Score with a different mathematical lens.

**AI-Powered Skill Verification**
Skills are not self-reported. Before any analysis runs, Google Gemini (gemini-2.5-flash) generates 3 MCQ questions per selected skill calibrated to the exact level the student claimed (Beginner, Intermediate, or Advanced). Only skills where the student scores 2 or 3 correct are counted as Confirmed. Scoring 1 correct gives Borderline status with the level downgraded by one step.

**Proctoring System**
The quiz runs with webcam-based face detection using OpenCV Haar Cascade. If the student's face is missing for 5 or more continuous seconds, a violation is triggered. At 3 violations the quiz terminates automatically. Tab-switch and fullscreen-exit events are also detected via JavaScript injection.

**Career Track Matching**
Verified skills are compared against required_skills_per_track.csv to calculate match percentage for each of the 8 tracks. The highest match is declared the best-fit track. Gap analysis lists skills the student is missing for that track sorted by job market frequency.

**Next Skill Recommendation**
The single highest-frequency missing skill from the best-fit track is surfaced as the one thing to learn next. A job readiness gauge chart shows the student's readiness score (0-100) calculated using weighted skill importance.

**Urgency Engine and Focus Debt**
Calculates weeks remaining before the student's likely placement season based on their semester. Shows how much of the student's effort has been spent on skills that do not belong to their best-fit track (Focus Debt).

**Peer Placement Rate**
Maps the student's Drift Score to an estimated placement rate using NASSCOM and AICTE outcome data. Students with Drift 0-20 show 78% estimated placement rate. Students with Drift 80-100 show 18%.

**Faculty Batch Dashboard**
Faculty upload up to 100 student CSV report files. The system re-runs all 8 calculations fresh for every student from their raw verified skills. No student can inflate results — everything is recalculated server-side regardless of what the downloaded CSV contained.

**Persistent Session with URL-Based Restore**
Each student gets a UUID4 session ID written to the URL as `?sid=...`. On browser refresh, the same session is restored from a disk JSON file. All 8 calculation results are computed once after quiz submission and reused on every dashboard page without recalculation.

---

## Real Data Behind the Platform

The platform was built using data collected manually from Naukri.com.

| Dataset                 | Details                                                                                                                                                                    |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Total job descriptions  | 1,600 (200 per career track)                                                                                                                                               |
| Unique companies        | 246                                                                                                                                                                        |
| Cities covered          | 18 (Bangalore, Hyderabad, Pune, Mumbai, Chennai, Noida, Gurugram, Ahmedabad, Kolkata, Jaipur, Indore, Bhopal, Surat, Delhi, Coimbatore, Thane, Remote, Thiruvananthapuram) |
| Experience levels       | Fresher, 0-1 Yrs, 0-2 Yrs, 0-3 Yrs — all entry level                                                                                                                      |
| Unique skills extracted | 142                                                                                                                                                                        |
| NLP tools used          | Python, Pandas, regex, 200+ alias normalization dictionary                                                                                                                 |

**Processed CSV files powering all calculations:**

- `required_skills_per_track.csv` — 179 rows, 3 columns (track, skill, frequency_pct). What skills each track requires and how often they appear across 200 JDs for that track.
- `skills_mapping.csv` — 142 skills as rows, 8 career track columns as binary (0/1). Which tracks each skill belongs to.
- `city_job_counts.csv` — 17 cities as rows, 8 career track job count columns plus latitude and longitude. Used for the India map.

---

## Tech Stack

| Technology            | Version   | Purpose                                                                      |
| --------------------- | --------- | ---------------------------------------------------------------------------- |
| Python                | 3.13      | Core programming language for all logic, data processing, and math           |
| Streamlit             | >= 1.40.0 | Web application framework — converts Python scripts to UI pages             |
| Pandas                | >= 2.2.3  | Reads and processes all CSV data files, builds DataFrames for display        |
| NumPy                 | >= 2.2.0  | Array operations for Drift Score — std deviation, normalization, clipping   |
| SciPy                 | >= 1.15.0 | Shannon Entropy calculation (scipy.stats.entropy) for Entropy Score          |
| Plotly                | 5.22.0    | All interactive charts — bar, radar, gauge, grouped bar, choropleth map     |
| Google Generative AI  | 1.73.1    | Gemini 2.5 Flash API for quiz question generation per skill per level        |
| streamlit-webrtc      | >= 0.47.0 | Real-time webcam access inside Streamlit for proctoring                      |
| OpenCV (headless)     | >= 4.8.0  | Haar Cascade face detection on webcam frames for violation tracking          |
| PyAV                  | >= 11.0.0 | FFmpeg bindings required by streamlit-webrtc to decode video frames          |
| streamlit-autorefresh | >= 1.0.1  | Auto-refresh for live updates during quiz and proctoring                     |
| Hashlib               | stdlib    | SHA-256 password hashing for faculty credential storage                      |
| UUID                  | stdlib    | UUID4 session ID generation for URL-based session persistence                |
| JSON                  | stdlib    | Disk-based session state persistence (data/sessions/*.json)                  |
| Threading             | stdlib    | Thread-safe access to shared proctoring state between WebRTC and main thread |
| Pathlib               | stdlib    | Cross-platform file path management for session storage directory            |
| Collections.Counter   | stdlib    | Most common missing skills across batch-uploaded student files               |

---

## Project Structure

```
SkillDrift/
│
├── app.py                          # Entry point — sets page config, init session, routes to home
├── brain.py                        # Calculation engine — all scoring math and business logic
├── gemini_quiz.py                  # AI quiz system — prompt building, Gemini API calls, scoring
├── proctor.py                      # Proctoring system — face detection, violation tracking
├── session_store.py                # Session management — UUID-based disk persistence
├── _sidebar.py                     # Shared sidebar — APPLE_CSS, nav, radar chart, scores
├── requirements.txt                # All Python package dependencies
│
├── pages/
│   ├── 01_home.py                  # Landing page — stats, how it works, faculty login button
│   ├── 02_skill_input.py           # Skill input form — name, semester, skill tabs, levels
│   ├── 02b_quiz.py                 # Quiz page — Gemini questions, proctoring overlay
│   ├── 03_drift_score.py           # Dashboard — quiz results table, drift score, entropy, chart
│   ├── 04_urgency.py               # Urgency Engine — semester timeline, focus debt
│   ├── 05_career_match.py          # Career match — bar chart, gap analysis table
│   ├── 06_next_skill.py            # Next skill — recommendation card, readiness gauge
│   ├── 07_peer_mirror.py           # Placement odds — peer comparison charts
│   ├── 08_market_intel.py          # Job market — India map, city-wise job counts
│   ├── 09_faculty.py               # Faculty login and dashboard
│   ├── 09b_student_view.py         # Faculty drill-down — individual student analysis
│   ├── 09c_batch_results.py        # Batch analytics — class-level charts and table
│   └── 10_final_report.py          # Report card — all scores, downloadable CSV
│
├── data/
│   ├── raw/
│   │   └── raw_jd_data.csv         # 1,600 job descriptions (role, company, skills, exp, city)
│   ├── processed/
│   │   ├── required_skills_per_track.csv
│   │   ├── skills_mapping.csv
│   │   └── city_job_counts.csv
│   ├── auth/
│   │   └── faculty_credentials.csv  # Faculty email and SHA-256 hashed passwords
│   └── sessions/                    # Auto-generated session JSON files (UUID named)
│
├── nlp_pipeline/
│   └── process_jd.py               # Offline NLP script — processes raw JD data into CSV files
│
├── reports/                         # Placeholder for generated report files
│
└── .streamlit/
    ├── config.toml                  # Theme — primaryColor #6C63FF, fonts, headless mode
    └── secrets.toml                 # Gemini API key — NOT committed to Git
```

---

## How to Run

### Step 1 — Prerequisites

Python 3.10 or higher is required. Python 3.13 was used in development.

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

Create the file `.streamlit/secrets.toml` with the following content. Do not commit this file to Git.

```toml
[gemini]
api_key = "your-gemini-api-key-here"
```

Get a free API key from [Google AI Studio](https://aistudio.google.com). No credit card is needed for the free tier.

### Step 6 — Run the application

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501` in your browser.

### Step 7 — Run the NLP pipeline (optional, only if you update raw job data)

```bash
python nlp_pipeline/process_jd.py
```

This regenerates the three processed CSV files from `raw_jd_data.csv`. Only needed if you replace or update the raw job description data.

---

## Complete Student Flow

1. Student opens the app. Session is created with a UUID4 ID written to the URL as `?sid=...`.
2. Student reads the home page and clicks **Analyze My Career Focus**.
3. Student enters their name, selects their semester, and picks skills with levels across 6 tabbed categories.
4. Gemini generates 3 MCQ questions per skill calibrated to the claimed level. A loading bar shows progress skill by skill.
5. Student takes the quiz with the webcam proctoring overlay active. Answers are radio buttons.
6. On submission, each skill is scored. Confirmed (2-3 correct), Borderline (1 correct, level downgraded), Not Verified (0 correct, excluded from analysis).
7. All 8 calculations run once from verified skills: Drift Score, Entropy, Career Match, Readiness Score, Next Skill, Urgency, Focus Debt, Peer Placement Rate.
8. Student navigates 8 dashboard pages via the sidebar. Each page reads from session state — no recalculation.
9. On the Report Card page, student downloads a CSV report file for submission to their faculty.
10. Student signs out. Session JSON is deleted from disk. URL is cleared.

---

## Complete Faculty Flow

1. Faculty clicks **Faculty Login** on the home page and enters email and password.
2. Credentials are verified by SHA-256 hashing the entered password and comparing to the stored hash in `faculty_credentials.csv`.
3. Faculty selects up to 100 student CSV report files using the batch uploader.
4. The system parses each file and re-runs all 8 calculations fresh from raw verified skills. No student can inflate results because everything is recalculated server-side.
5. Batch analytics page shows class average drift score, readiness score, urgency level distribution (Red / Yellow / Green), top 5 missing skills across all students, and a sortable per-student table.
6. Faculty clicks any student row to view the full individual analysis drill-down.
7. Faculty downloads a batch CSV report for institutional records.

---

## Scoring Algorithms

**Drift Score**

```
track_array = array of skill counts for each of the 8 career tracks
std_dev = numpy.std(track_array)
max_std = std_dev of [total_skills, 0, 0, 0, 0, 0, 0, 0]  (maximum possible concentration)
drift_score = numpy.clip((std_dev / max_std) * 100, 0, 100)
```

A student fully focused on one track scores near 0. A student evenly spread across all tracks scores near 100.

**Entropy Score**

```
entropy_score = (drift_score / 100) * 3.0  (in bits, max 3.0 bits)
```

Derived from drift score using linear mapping for consistency. Higher entropy means more disorder in the skill distribution.

**Career Match Percentage**

```
For each track:
  matched = count of verified skills that appear in required_skills_per_track for this track
  total_required = count of required skills for this track
  match_pct = (matched / total_required) * 100
```

**Readiness Score**

```
For best-fit track:
  For each verified skill in this track:
    score += frequency_pct of that skill (from required_skills_per_track)
  readiness = numpy.clip((score / max_possible_score) * 100, 0, 100)
```

**Peer Placement Rate (lookup table from NASSCOM and AICTE data)**

| Drift Score Range | Estimated Placement Rate |
| ----------------- | ------------------------ |
| 0 - 20            | 78%                      |
| 20 - 40           | 62%                      |
| 40 - 60           | 44%                      |
| 60 - 80           | 29%                      |
| 80 - 100          | 18%                      |

---

## Security

- Faculty passwords are stored as SHA-256 hashes in `faculty_credentials.csv`. Plain text passwords are never stored anywhere.
- The Gemini API key is stored in `.streamlit/secrets.toml` which is listed in `.gitignore` and never committed to the repository.
- Session IDs are UUID4 hex strings (32 random hexadecimal characters). Session data is stored on the server disk, not in the browser. Students cannot tamper with session data.
- Quiz answers are persisted per session key (`q_X_Y` format) so a refresh during the quiz restores already-answered questions without allowing re-entry.
- Session files older than 7 days are automatically garbage collected from `data/sessions/`.

---

## Configuration

`/.streamlit/config.toml` controls the visual theme and server behavior:

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

| ID    | Feature                                                                                               |
| ----- | ----------------------------------------------------------------------------------------------------- |
| FS-01 | Live Job API Integration — real-time job data instead of manually collected CSVs                     |
| FS-02 | Redis-Based Session Store — replace disk JSON sessions with Redis for scalability                    |
| FS-03 | Advanced Liveness Detection — replace Haar Cascade with deep learning-based face detection           |
| FS-04 | Mentor Review Layer — allow mentors to annotate student reports before faculty view                  |
| FS-05 | Native Mobile App — iOS and Android wrapper around the Streamlit backend                             |
| FS-06 | Blockchain Skill Certificates — tamper-proof certificate issuance for verified skills                |
| FS-07 | Institution Portal — multi-department support for university-wide deployment                         |
| FS-08 | Peer Benchmarking — compare a student's scores against anonymized batch averages                     |
| FS-09 | Learning Path Integration — link recommended skills to specific free courses on platforms like NPTEL |
| FS-10 | Multilingual Support — Hindi and regional language UI for broader student access                     |

---

## Known Limitations

| ID   | Limitation                                                                                                                |
| ---- | ------------------------------------------------------------------------------------------------------------------------- |
| L-01 | Proctoring uses Haar Cascade (OpenCV) which has higher false-negative rate than deep learning models                      |
| L-02 | Job data is a static snapshot from Naukri collected in early 2026. Market shifts are not reflected in real time.          |
| L-03 | First load is slow because Streamlit re-imports all modules and loads the Gemini model client                             |
| L-04 | If deployed on free-tier cloud with inactivity timeout, the session JSON files are wiped on restart                       |
| L-05 | Large batch uploads (80-100 files) can take 30+ seconds to process on low-spec servers                                    |
| L-06 | Gemini-generated questions are AI-generated and may occasionally be repetitive for very common skills                     |
| L-07 | No real-time recruiter notification or LinkedIn integration                                                               |
| L-08 | Mentor review layer is designed but not implemented in the current version                                                |
| L-09 | No dedicated mobile app — the Streamlit UI is responsive but not natively optimized for small screens                    |
| L-10 | Niche roles (Blockchain, AR/VR, Embedded Systems) are not among the 8 tracks due to low fresher JD availability on Naukri |

---

## References

1. NASSCOM, "Technology Sector in India — Annual Report 2024," National Association of Software and Service Companies, New Delhi, 2024.
2. Wheebox and Mercer Mettl, "India Skills Report 2024," Wheebox Employability Test, Gurugram, 2024.
3. AICTE, "All India Council for Technical Education — Annual Statistical Report 2023-24," AICTE, New Delhi, 2024.
4. C. E. Shannon, "A Mathematical Theory of Communication," Bell System Technical Journal, vol. 27, pp. 379-423, 1948.
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
| Batch                  | 2022-2026                                               |
| Semester               | VIII, Section D                                         |
| Project Start          | 29th January, 2026                                      |
| Project End            | 30th April, 2026                                        |
| Guide                  | Dr. Avinash Kumar, Assistant Professor, CSE, SBU        |
| Dean FoECS             | Dr. Pankaj Kr Goswami                                   |
| Associate Dean and HoD | Dr. Priyanka Srivastava                                 |
| Program Coordinator    | Dr. Ashish Sinha                                        |
