"""
main.py — CLI entry point for the Résumé × JD Analyser.

This module connects document parsing, LLM analysis, score aggregation,
and report generation into one command-line pipeline.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from analyzer import (
    analyse_background_fit,
    analyse_bullets,
    analyse_jargon,
    analyse_keyword_match,
    analyse_structure,
    compute_overall_score,
    extract_jd_profile,
    extract_resume_profile,
    summarise_overall,
)
from parse import read_jd_text, read_resume_pdf
from report import render_markdown


ATS_PASS_THRESHOLD = 60


def parse_args(argv: list[str]) -> tuple[str, str]:
    """
    Parse the résumé and job-description command-line arguments.

    Args:
        argv: Complete command-line argument list.

    Returns:
        Tuple containing the résumé PDF path and job-description text path.
    """
    parser = argparse.ArgumentParser(
        prog="python main.py",
        description="Résumé × JD Analyser — diagnostic feedback only.",
    )

    parser.add_argument(
        "resume",
        metavar="resume.pdf",
        help="Path to the PDF résumé.",
    )

    parser.add_argument(
        "job",
        metavar="job.txt",
        help="Path to the plain-text job description.",
    )

    args = parser.parse_args(argv[1:])
    return args.resume, args.job


def main() -> int:
    """
    Run the complete résumé and job-description analysis pipeline.

    Returns:
        Zero when the analysis succeeds or one when an error occurs.
    """
    resume_path, job_path = parse_args(sys.argv)

    model = os.getenv("MODEL", "openai/gpt-4o-mini")
    print(f"Using model: {model}")

    print(f"[1/8] Parsing résumé: {resume_path}")

    try:
        resume_text = read_resume_pdf(resume_path)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"[2/8] Reading JD: {job_path}")

    try:
        jd_text = read_jd_text(job_path)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    try:
        print("[3/8] Extracting résumé profile (LLM)...")
        resume_profile = extract_resume_profile(resume_text)

        print("[4/8] Extracting JD profile (LLM)...")
        jd_profile = extract_jd_profile(jd_text)

        print("[5/8] Keyword match (LLM)...")
        keyword_match = analyse_keyword_match(
            resume_profile,
            jd_profile,
        )

        print("[6/8] Bullet audit (LLM)...")
        bullets = analyse_bullets(resume_profile)

        print("[7/8] Jargon, structure, background fit (LLM x3)...")
        jargon = analyse_jargon(
            resume_profile,
            jd_profile,
        )

        structure = analyse_structure(resume_text)

        background_fit = analyse_background_fit(
            resume_profile,
            jd_profile,
        )

    except RuntimeError as error:
        print(f"LLM analysis failed: {error}", file=sys.stderr)
        return 1
    except Exception as error:
        print(
            f"Unexpected analysis error: {error}",
            file=sys.stderr,
        )
        return 1

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report = {
        "meta": {
            "model": model,
            "resume_path": resume_path,
            "job_description_path": job_path,
            "generated_at": timestamp,
            "ats_pass_threshold": ATS_PASS_THRESHOLD,
        },
        "resume_profile": resume_profile,
        "jd_profile": jd_profile,
        "keyword_match": keyword_match,
        "bullets": bullets,
        "jargon": jargon,
        "structure": structure,
        "background_fit": background_fit,
    }

    overall_score = compute_overall_score(report)

    report["overall_score"] = overall_score
    report["passes_ats_threshold"] = (
        overall_score >= ATS_PASS_THRESHOLD
    )

    try:
        print("[8/8] Final summary (LLM)...")
        report["summary"] = summarise_overall(report)
    except RuntimeError as error:
        print(f"Summary generation failed: {error}", file=sys.stderr)
        return 1
    except Exception as error:
        print(
            f"Unexpected summary error: {error}",
            file=sys.stderr,
        )
        return 1

    output_directory = Path("outputs")
    output_directory.mkdir(parents=True, exist_ok=True)

    json_path = (
        output_directory
        / f"match_report_{timestamp}.json"
    )

    markdown_path = (
        output_directory
        / f"match_report_{timestamp}.md"
    )

    try:
        json_path.write_text(
            json.dumps(
                report,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        render_markdown(
            report,
            out_path=markdown_path,
        )

    except OSError as error:
        print(
            f"Could not write report files: {error}",
            file=sys.stderr,
        )
        return 1
    except Exception as error:
        print(
            f"Report generation failed: {error}",
            file=sys.stderr,
        )
        return 1

    verdict = (
        "PASS"
        if report["passes_ats_threshold"]
        else "FAIL"
    )

    print()
    print(
        f"Score: {overall_score}/100 "
        f"({verdict} {ATS_PASS_THRESHOLD}% ATS threshold)"
    )
    print(f"JSON:  {json_path}")
    print(f"MD:    {markdown_path}")
    print()
    print(report["summary"])

    return 0


if __name__ == "__main__":
    sys.exit(main())