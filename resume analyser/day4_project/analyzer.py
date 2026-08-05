"""
analyzer.py — the analysis functions and pure-Python score calculator.
"""

import json

from llm import ask_json, ask_text
from prompts import (
    RESUME_PROFILE_PROMPT,
    JD_PROFILE_PROMPT,
    KEYWORD_MATCH_PROMPT,
    BULLET_QUALITY_PROMPT,
    JARGON_AUDIT_PROMPT,
    STRUCTURE_AUDIT_PROMPT,
    BACKGROUND_FIT_PROMPT,
    OVERALL_SUMMARY_PROMPT,
)


def extract_resume_profile(resume_text: str) -> dict:
    """Convert plain résumé text into a structured candidate profile."""
    user = f"RÉSUMÉ TEXT:\n\n{resume_text}"

    return ask_json(
        RESUME_PROFILE_PROMPT,
        user,
        temperature=0.0,
        max_tokens=2000,
    )


def extract_jd_profile(jd_text: str) -> dict:
    """Convert plain job-description text into a structured JD profile."""
    user = f"JOB DESCRIPTION TEXT:\n\n{jd_text}"

    return ask_json(
        JD_PROFILE_PROMPT,
        user,
        temperature=0.0,
        max_tokens=1500,
    )


def analyse_keyword_match(
    resume_profile: dict,
    jd_profile: dict,
) -> dict:
    """Compare résumé keywords against job-description requirements."""
    user = (
        "RÉSUMÉ PROFILE:\n"
        f"{json.dumps(resume_profile, ensure_ascii=False)}\n\n"
        "JD PROFILE:\n"
        f"{json.dumps(jd_profile, ensure_ascii=False)}"
    )

    return ask_json(
        KEYWORD_MATCH_PROMPT,
        user,
        temperature=0.2,
        max_tokens=1800,
    )


def analyse_bullets(resume_profile: dict) -> dict:
    """Score résumé bullets using the Action-Technology-Impact rubric."""
    compact_profile = {
        "projects": resume_profile.get("projects", []),
        "experience": resume_profile.get("experience", []),
    }

    user = (
        "RÉSUMÉ PROFILE:\n"
        f"{json.dumps(compact_profile, ensure_ascii=False)}"
    )

    result = ask_json(
        BULLET_QUALITY_PROMPT,
        user,
        temperature=0.1,
        max_tokens=1800,
    )

    bullets = result.get("bullets", [])

    level_values = {
        "L1_OK": 1,
        "L2_BETTER": 2,
        "L3_BEST": 3,
    }

    scores = []

    for bullet in bullets:
        if isinstance(bullet, dict):
            level = str(bullet.get("level", ""))
            scores.append(level_values.get(level, 0))

    if scores:
        result["bullet_quality_avg"] = round(
            100 * sum(scores) / (3 * len(scores))
        )
    else:
        result["bullet_quality_avg"] = 0

    return result


def analyse_jargon(
    resume_profile: dict,
    jd_profile: dict,
) -> dict:
    """Identify terminology differences between the résumé and JD."""
    user = (
        "RÉSUMÉ PROFILE:\n"
        f"{json.dumps(resume_profile, ensure_ascii=False)}\n\n"
        "JD PROFILE:\n"
        f"{json.dumps(jd_profile, ensure_ascii=False)}"
    )

    return ask_json(
        JARGON_AUDIT_PROMPT,
        user,
        temperature=0.2,
        max_tokens=1500,
    )


def analyse_structure(resume_text: str) -> dict:
    """Audit the résumé for general ATS parseability."""
    user = f"RÉSUMÉ TEXT:\n\n{resume_text}"

    return ask_json(
        STRUCTURE_AUDIT_PROMPT,
        user,
        temperature=0.0,
        max_tokens=1500,
    )


def analyse_background_fit(
    resume_profile: dict,
    jd_profile: dict,
) -> dict:
    """Assess whether the candidate's background aligns with the role."""
    user = (
        "RÉSUMÉ PROFILE:\n"
        f"{json.dumps(resume_profile, ensure_ascii=False)}\n\n"
        "JD PROFILE:\n"
        f"{json.dumps(jd_profile, ensure_ascii=False)}"
    )

    return ask_json(
        BACKGROUND_FIT_PROMPT,
        user,
        temperature=0.2,
        max_tokens=600,
    )


def summarise_overall(report: dict) -> str:
    """Generate a three-bullet Markdown summary of the screening report."""
    summary_input = {
        "overall_score": report.get("overall_score", 0),
        "passes_ats_threshold": report.get(
            "passes_ats_threshold",
            False,
        ),
        "keyword_match": report.get("keyword_match", {}),
        "bullets": report.get("bullets", {}),
        "jargon": report.get("jargon", {}),
        "structure": report.get("structure", {}),
        "background_fit": report.get("background_fit", {}),
    }

    user = (
        "ANALYSIS REPORT:\n"
        f"{json.dumps(summary_input, ensure_ascii=False)}"
    )

    return ask_text(
        OVERALL_SUMMARY_PROMPT,
        user,
        temperature=0.3,
        max_tokens=400,
    ).strip()


def compute_overall_score(report: dict) -> int:
    """Calculate the weighted overall ATS score."""
    keyword_score = report.get(
        "keyword_match",
        {},
    ).get(
        "keyword_match_score",
        0,
    )

    bullet_score = report.get(
        "bullets",
        {},
    ).get(
        "bullet_quality_avg",
        0,
    )

    structure_score = report.get(
        "structure",
        {},
    ).get(
        "structure_score",
        0,
    )

    jargon_score = report.get(
        "jargon",
        {},
    ).get(
        "jargon_score",
        0,
    )

    background_score = report.get(
        "background_fit",
        {},
    ).get(
        "background_fit_score",
        0,
    )

    total = (
        keyword_score * 0.40
        + bullet_score * 0.25
        + structure_score * 0.15
        + jargon_score * 0.10
        + background_score * 0.10
    )

    return int(round(total))