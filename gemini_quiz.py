# =============================================================
# gemini_quiz.py — SkillDrift Gemini Quiz Engine
# Handles all Gemini API interaction for skill verification.
# Called only from pages/02_skill_input.py
# =============================================================

import json
import re
import time
import streamlit as st
from google import genai

# =============================================================
# SECTION 1 — CONFIGURE GEMINI API
# =============================================================

def configure_gemini():
    """
    Configures the Gemini API client using the key from secrets.
    Returns True if configured successfully, False otherwise.
    """
    try:
        api_key = st.secrets["gemini"]["api_key"]
        st.session_state["gemini_client"] = genai.Client(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Gemini API configuration failed: {str(e)}")
        return False


# =============================================================
# SECTION 2 — PROMPT BUILDER
# =============================================================

def build_quiz_prompt(skill: str, level: str) -> str:
    """
    Builds the prompt sent to Gemini for a given skill and level.
    Returns 2 MCQs in strict JSON format.
    """
    prompt = f"""You are an expert technical interviewer for Indian CSE placement preparation.

Generate exactly 3 multiple choice questions to test a B.Tech CSE student's knowledge of {skill} at {level} level.

Rules:
- Questions must be practical and specific to {skill}
- Difficulty must match {level} level exactly
- Each question must have exactly 4 options: A, B, C, D
- Exactly one option must be correct
- The correct answers must be randomly distributed among A, B, C, and D
- Do NOT repeat the same correct option more than twice
- Output MUST contain exactly 3 questions (no more, no less)

Output format (STRICT JSON, no extra text):

[
  {{
    "question": "Question 1?",
    "option_a": "Option A",
    "option_b": "Option B",
    "option_c": "Option C",
    "option_d": "Option D",
    "correct": "A"
  }},
  {{
    "question": "Question 2?",
    "option_a": "Option A",
    "option_b": "Option B",
    "option_c": "Option C",
    "option_d": "Option D",
    "correct": "B"
  }},
  {{
    "question": "Question 3?",
    "option_a": "Option A",
    "option_b": "Option B",
    "option_c": "Option C",
    "option_d": "Option D",
    "correct": "C"
  }}
]

Constraints:
- The "correct" field must be exactly one of: A, B, C, or D (uppercase only)
- Return ONLY the JSON array
- No explanation
- No markdown
- No code block
- No trailing commas
"""

    return prompt


# =============================================================
# SECTION 3 — GEMINI API CALLER WITH SAFETY WRAPPER
#
# Uses gemini-2.0-flash (current recommended free-tier model).
# Retries once on failure. Surfaces the real error in Streamlit
# instead of silently returning an empty list.
# =============================================================

# Primary model — gemini-2.0-flash is the current recommended free model
# (gemini-1.5-flash has free-tier quota restrictions in 2025)
GEMINI_MODEL = "gemini-2.5-flash"

def call_gemini_with_retry(prompt: str, skill: str) -> list:
    """
    Calls Gemini API and parses the JSON response.
    Retries once if the first response is malformed.
    Returns empty list if both attempts fail (skill marked Unverified).

    Parameters
    ----------
    prompt : str   The quiz prompt
    skill  : str   Skill name (for error messages only)

    Returns
    -------
    questions : list of dicts  (empty = both attempts failed)
    """

    # Get API key from Streamlit secrets
    try:
        api_key = st.secrets["gemini"]["api_key"]
    except Exception as e:
        st.error(
            f"❌ **Gemini API key missing or misconfigured.**\n\n"
            f"Check that `.streamlit/secrets.toml` has:\n"
            f"```\n[gemini]\napi_key = \"YOUR_KEY\"\n```\n\n"
            f"Error: {e}"
        )
        return []

    # Build client fresh each call (stateless, safe for Streamlit reruns)
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"❌ Could not create Gemini client: {e}")
        return []

    last_error = None

    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )
            raw_text = response.text.strip()
            questions = parse_gemini_response(raw_text, skill, attempt + 1)
            if questions:
                return questions
            # Parse succeeded but validation failed — retry
            if attempt == 0:
                time.sleep(1)

        except Exception as e:
            last_error = e
            if attempt == 0:
                # Wait and retry once
                time.sleep(2)
            else:
                # Both attempts failed — show the actual error
                st.warning(
                    f"⚠️ Gemini API error for **{skill}** "
                    f"({type(e).__name__}): {e}. "
                    f"Skill will be accepted as Unverified."
                )
                return []

    # Parse failed on both attempts (no exception, just bad JSON from Gemini)
    return []


def parse_gemini_response(raw_text: str, skill: str, attempt: int) -> list:
    """
    Parses Gemini's response as a JSON array.
    Handles markdown code fences and leading/trailing text.

    Returns questions list, or empty list if parsing fails.
    """

    # Remove markdown fences: ```json ... ``` or ``` ... ```
    cleaned = re.sub(r"```(?:json)?\s*", "", raw_text)
    cleaned = re.sub(r"```", "", cleaned)
    cleaned = cleaned.strip()

    # Strategy 1 — direct JSON parse
    try:
        questions = json.loads(cleaned)
        if validate_questions(questions):
            return questions
    except json.JSONDecodeError:
        pass

    # Strategy 2 — extract the first [...] block using regex
    array_match = re.search(r"\[.*?\]", cleaned, re.DOTALL)
    if array_match:
        try:
            questions = json.loads(array_match.group())
            if validate_questions(questions):
                return questions
        except json.JSONDecodeError:
            pass

    return []


def validate_questions(questions: list) -> bool:
    """
    Validates the parsed JSON has the correct structure.
    Returns True only if all required fields and valid correct letters exist.
    """
    if not isinstance(questions, list) or len(questions) != 3:
        return False

    required_keys = {"question", "option_a", "option_b", "option_c", "option_d", "correct"}

    for q in questions:
        if not isinstance(q, dict):
            return False
        if not required_keys.issubset(q.keys()):
            return False
        if str(q.get("correct", "")).upper() not in {"A", "B", "C", "D"}:
            return False

    return True


# =============================================================
# SECTION 4 — QUIZ SCORER
# =============================================================

def score_quiz_answers(skill: str, claimed_level: str,
                       questions: list, student_answers: list) -> dict:
    """
    Scores the student's answers for one skill.

    Scoring rules:
    - More than half correct  → Confirmed at claimed level
    - Exactly half correct    → Downgraded by one step
    - Fewer than half correct → Not Verified (excluded from analysis)
    - No questions generated  → Unverified (accepted as-is)
    """

    if not questions:
        return {
            "skill":           skill,
            "claimed_level":   claimed_level,
            "verified_level":  claimed_level,
            "status":          "Unverified",
            "correct_count":   0,
            "total_questions": 0,
        }

    total = len(questions)
    correct_count = 0

    for i, question in enumerate(questions):
        if i >= len(student_answers):
            break
        student_answer = str(student_answers[i]).upper().strip()
        correct_answer = str(question.get("correct", "")).upper().strip()
        if student_answer == correct_answer:
            correct_count += 1

    ratio = correct_count / total

    if ratio >= 0.67:  # 2/3 or 3/3
        status = "Confirmed"
        verified_level = claimed_level

    elif ratio >= 0.34:  # 1/3
        status = "Borderline"
        if claimed_level == "Beginner":
            verified_level = "Beginner"
        else:
            verified_level = downgrade_level(claimed_level)

    else:  # 0/3
        status = "Not Verified"
        verified_level = "Not Verified"

    return {
        "skill":           skill,
        "claimed_level":   claimed_level,
        "verified_level":  verified_level,
        "status":          status,
        "correct_count":   correct_count,
        "total_questions": total,
    }


def downgrade_level(level: str) -> str:
    """
    Advanced → Intermediate → Beginner → Beginner
    """
    downgrade_map = {
        "Advanced": "Intermediate",
        "Intermediate": "Beginner",
        "Beginner": "Beginner",
    }
    return downgrade_map.get(level, "Beginner")


# =============================================================
# SECTION 5 — FULL QUIZ RUNNER
# Called once from 02_skill_input.py after skill submission.
# =============================================================

def run_skill_verification_quiz(selected_skills: dict) -> dict:

    if not configure_gemini():
        st.error("Cannot run quiz — Gemini API not configured.")
        return {}

    st.markdown("---")
    st.subheader("🎯 Skill Verification Quiz")
    st.markdown(
        "Answer these questions honestly. Your analysis depends on accurate results. "
        "**This quiz verifies whether you actually know what you claimed.**"
    )

    # ✅ Generate quiz only once
    selected_sig = tuple(sorted(selected_skills.items()))

    if "quiz_data_sig" not in st.session_state or st.session_state["quiz_data_sig"] != selected_sig:
        with st.spinner(f"Generating quiz questions using Gemini AI (model: {GEMINI_MODEL})..."):

            st.session_state["quiz_data"] = []

            for skill, level in selected_skills.items():
                prompt = build_quiz_prompt(skill, level)
                questions = call_gemini_with_retry(prompt, skill)

                st.session_state["quiz_data"].append({
                    "skill": skill,
                    "level": level,
                    "questions": questions,
                })

                time.sleep(0.5)

        st.session_state["quiz_data_sig"] = selected_sig

    all_quiz_data = st.session_state["quiz_data"]

    # Display questions and collect answers
    st.markdown("---")
    student_responses = {}

    for quiz_item in all_quiz_data:
        skill = quiz_item["skill"]
        level = quiz_item["level"]
        questions = quiz_item["questions"]

        if not questions:
            st.warning(
                f"⚠️ Could not generate questions for **{skill}**. "
                f"It will be accepted as **Unverified**."
            )
            student_responses[skill] = []
            continue

        st.markdown(f"### {skill} — {level} Level")

        answers_for_skill = []
        for q_idx, q in enumerate(questions):
            st.markdown(f"**Q{q_idx + 1}. {q['question']}**")

            options = {
                "A": q["option_a"],
                "B": q["option_b"],
                "C": q["option_c"],
                "D": q["option_d"],
            }

            option_labels = [f"{k}: {v}" for k, v in options.items()]
            selected = st.radio(
                label=f"Select your answer:",
                options=option_labels,
                key=f"quiz_{skill}_{q_idx}",
                index=None,
            )

            answer_letter = selected[0] if selected else None
            answers_for_skill.append(answer_letter)
            st.markdown("")

        student_responses[skill] = answers_for_skill
        st.markdown("---")

    # Submit button
    submit_quiz = st.button(
        "✅ Submit Quiz and See My Results",
        type="primary",
        width="stretch",
    )

    if not submit_quiz:
        return {}

    # Check all questions answered
    unanswered = []
    for quiz_item in all_quiz_data:
        skill = quiz_item["skill"]
        if not quiz_item["questions"]:
            continue
        answers = student_responses.get(skill, [])
        if None in answers or len(answers) < len(quiz_item["questions"]):
            unanswered.append(skill)

    if unanswered:
        st.error(
            f"Please answer all questions before submitting. "
            f"Unanswered skills: {', '.join(unanswered)}"
        )
        return {}

    # Score all answers
    quiz_results = []
    verified_skills = {}

    for quiz_item in all_quiz_data:
        skill     = quiz_item["skill"]
        level     = quiz_item["level"]
        questions = quiz_item["questions"]
        answers   = student_responses.get(skill, [])

        result = score_quiz_answers(skill, level, questions, answers)
        quiz_results.append(result)

        if result["verified_level"] != "Not Verified":
            verified_skills[skill] = result["verified_level"]
    if not verified_skills:
        for r in quiz_results:
            verified_skills[r["skill"]] = r["claimed_level"]
    st.session_state["quiz_results"] = quiz_results
    st.session_state["verified_skills"] = verified_skills
    st.session_state["quiz_complete"] = True

    st.success("Quiz submitted successfully.")
    return verified_skills                       # ← ADD THIS
