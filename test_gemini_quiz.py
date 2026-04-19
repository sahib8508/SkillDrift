# =============================================================
# test_gemini_quiz.py — Tests for gemini_quiz.py
# Tests only the logic functions (no Streamlit UI, no API call)
# Run with: python test_gemini_quiz.py
# =============================================================

import sys

def run_test(name, func):
    try:
        func()
        print(f"  ✅ PASS — {name}")
    except Exception as e:
        print(f"  ❌ FAIL — {name}: {e}")

print()
print("=" * 60)
print("  SKILLDRIFT — gemini_quiz.py TEST SUITE")
print("=" * 60)

from gemini_quiz import (
    build_quiz_prompt,
    parse_gemini_response,
    validate_questions,
    score_quiz_answers,
    downgrade_level,
    configure_gemini,
)

print()
print("[ STEP 1 ] Testing build_quiz_prompt()...")

def test_prompt_contains_skill():
    prompt = build_quiz_prompt("SQL", "Intermediate")
    assert "SQL" in prompt
    assert "Intermediate" in prompt
    assert "JSON" in prompt
    print(f"           Prompt length: {len(prompt)} chars ✅")

run_test("build_quiz_prompt() contains skill and level", test_prompt_contains_skill)

print()
print("[ STEP 2 ] Testing validate_questions()...")

VALID_QUESTIONS = [
    {
        "question": "What does SQL stand for?",
        "option_a": "Structured Query Language",
        "option_b": "Simple Query Language",
        "option_c": "Standard Query Logic",
        "option_d": "Sequential Query Language",
        "correct": "A"
    },
    {
        "question": "Which SQL clause filters rows?",
        "option_a": "GROUP BY",
        "option_b": "ORDER BY",
        "option_c": "WHERE",
        "option_d": "HAVING",
        "correct": "C"
    }
]

def test_valid_structure():
    assert validate_questions(VALID_QUESTIONS) is True
    print(f"           Valid structure accepted ✅")

def test_empty_list():
    assert validate_questions([]) is False
    print(f"           Empty list rejected ✅")

def test_missing_key():
    bad = [{"question": "test?", "option_a": "a", "correct": "A"}]
    assert validate_questions(bad) is False
    print(f"           Missing keys rejected ✅")

def test_invalid_correct():
    bad = [dict(VALID_QUESTIONS[0])]
    bad[0]["correct"] = "E"
    assert validate_questions(bad) is False
    print(f"           Invalid correct letter rejected ✅")

run_test("validate_questions() — valid structure", test_valid_structure)
run_test("validate_questions() — empty list", test_empty_list)
run_test("validate_questions() — missing keys", test_missing_key)
run_test("validate_questions() — invalid correct letter", test_invalid_correct)

print()
print("[ STEP 3 ] Testing parse_gemini_response()...")

def test_clean_json():
    raw = '[{"question":"Q?","option_a":"A","option_b":"B","option_c":"C","option_d":"D","correct":"A"},{"question":"Q2?","option_a":"A","option_b":"B","option_c":"C","option_d":"D","correct":"B"}]'
    result = parse_gemini_response(raw, "SQL", 1)
    assert len(result) == 2
    print(f"           Clean JSON parsed: {len(result)} questions ✅")

def test_markdown_wrapped_json():
    raw = '```json\n[{"question":"Q?","option_a":"A","option_b":"B","option_c":"C","option_d":"D","correct":"A"},{"question":"Q2?","option_a":"A","option_b":"B","option_c":"C","option_d":"D","correct":"B"}]\n```'
    result = parse_gemini_response(raw, "SQL", 1)
    assert len(result) == 2
    print(f"           Markdown-wrapped JSON parsed: {len(result)} questions ✅")

def test_garbage_response():
    raw = "Sorry I cannot generate questions for this topic."
    result = parse_gemini_response(raw, "SQL", 1)
    assert result == []
    print(f"           Garbage response returns empty list ✅")

run_test("parse_gemini_response() — clean JSON", test_clean_json)
run_test("parse_gemini_response() — markdown wrapped", test_markdown_wrapped_json)
run_test("parse_gemini_response() — garbage response", test_garbage_response)

print()
print("[ STEP 4 ] Testing downgrade_level()...")

def test_downgrade_chain():
    assert downgrade_level("Advanced")     == "Intermediate"
    assert downgrade_level("Intermediate") == "Beginner"
    assert downgrade_level("Beginner")     == "Not Verified"
    assert downgrade_level("Unknown")      == "Not Verified"
    print(f"           Advanced→Intermediate→Beginner→Not Verified ✅")

run_test("downgrade_level() — full chain", test_downgrade_chain)

print()
print("[ STEP 5 ] Testing score_quiz_answers()...")

def test_all_correct():
    result = score_quiz_answers("SQL", "Intermediate", VALID_QUESTIONS, ["A", "C"])
    assert result["status"] == "Confirmed"
    assert result["verified_level"] == "Intermediate"
    assert result["correct_count"] == 2
    print(f"           2/2 correct → Confirmed at Intermediate ✅")

def test_half_correct():
    result = score_quiz_answers("SQL", "Intermediate", VALID_QUESTIONS, ["A", "A"])
    assert result["status"] == "Downgraded"
    assert result["verified_level"] == "Beginner"
    assert result["correct_count"] == 1
    print(f"           1/2 correct → Downgraded to Beginner ✅")

def test_none_correct():
    result = score_quiz_answers("SQL", "Intermediate", VALID_QUESTIONS, ["B", "A"])
    assert result["status"] == "Not Verified"
    assert result["verified_level"] == "Not Verified"
    assert result["correct_count"] == 0
    print(f"           0/2 correct → Not Verified ✅")

def test_no_questions():
    result = score_quiz_answers("SQL", "Advanced", [], [])
    assert result["status"] == "Unverified"
    assert result["verified_level"] == "Advanced"
    print(f"           No questions → Unverified (accepted) ✅")

def test_advanced_downgraded():
    result = score_quiz_answers("Python", "Advanced", VALID_QUESTIONS, ["A", "A"])
    assert result["status"] == "Downgraded"
    assert result["verified_level"] == "Intermediate"
    print(f"           1/2 correct at Advanced → Downgraded to Intermediate ✅")

run_test("score_quiz_answers() — all correct", test_all_correct)
run_test("score_quiz_answers() — half correct (downgrade)", test_half_correct)
run_test("score_quiz_answers() — none correct (not verified)", test_none_correct)
run_test("score_quiz_answers() — no questions (unverified)", test_no_questions)
run_test("score_quiz_answers() — advanced downgraded", test_advanced_downgraded)

print()
print("=" * 60)
print("  TEST SUITE COMPLETE")
print("=" * 60)
print()
print("  If all tests show ✅ PASS — gemini_quiz.py logic is ready.")
print("  The Streamlit UI functions require a running app to test.")
print()


