import streamlit as st
from dotenv import load_dotenv

from parse import read_resume_pdf
from analyzer import (
    extract_resume_profile,
    extract_jd_profile,
    analyse_keyword_match,
    analyse_bullets,
    analyse_jargon,
    analyse_structure,
    analyse_background_fit,
    summarise_overall,
    compute_overall_score,
)

load_dotenv()

st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide",
)

st.title("📄 AI Resume Analyzer")
st.write("Upload a résumé and paste a job description to generate an ATS analysis.")

resume_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"],
)

jd_text = st.text_area(
    "Paste Job Description",
    height=250,
)

run = st.button("Analyze Resume", type="primary")

if run:
    if resume_file is None:
        st.error("Please upload a résumé PDF.")
        st.stop()

    if not jd_text.strip():
        st.error("Please paste a job description.")
        st.stop()

    try:
        progress = st.progress(0, text="Reading résumé PDF...")

        # Step 1
        resume_text = read_resume_pdf(resume_file)
        progress.progress(10, text="Extracting résumé profile...")

        # Step 2
        resume_profile = extract_resume_profile(resume_text)
        progress.progress(25, text="Extracting job description profile...")

        # Step 3
        jd_profile = extract_jd_profile(jd_text)
        progress.progress(40, text="Analysing keyword match...")

        # Step 4
        keyword_match = analyse_keyword_match(
            resume_profile,
            jd_profile,
        )
        progress.progress(55, text="Analysing résumé bullets...")

        # Step 5
        bullets = analyse_bullets(resume_profile)
        progress.progress(65, text="Analysing terminology and jargon...")

        # Step 6
        jargon = analyse_jargon(
            resume_profile,
            jd_profile,
        )
        progress.progress(75, text="Analysing résumé structure...")

        # Step 7
        structure = analyse_structure(resume_text)
        progress.progress(85, text="Analysing background fit...")

        background_fit = analyse_background_fit(
            resume_profile,
            jd_profile,
        )

        report = {
            "resume_profile": resume_profile,
            "jd_profile": jd_profile,
            "keyword_match": keyword_match,
            "bullets": bullets,
            "jargon": jargon,
            "structure": structure,
            "background_fit": background_fit,
        }

        report["overall_score"] = compute_overall_score(report)
        report["passes_ats_threshold"] = report["overall_score"] >= 60

        progress.progress(95, text="Generating final summary...")

        # Step 8
        report["summary"] = summarise_overall(report)

        progress.progress(100, text="Analysis complete.")

    except ValueError as exc:
        st.error(f"File error: {exc}")
        st.stop()

    except RuntimeError as exc:
        st.error(f"Analysis error: {exc}")
        st.stop()

    except Exception as exc:
        st.error(f"Unexpected error: {exc}")
        st.exception(exc)
        st.stop()

    score = report["overall_score"]
    passed = report["passes_ats_threshold"]

    st.divider()
    st.header("Analysis Results")

    score_column, verdict_column = st.columns(2)

    with score_column:
        st.metric(
            label="Overall Score",
            value=f"{score}/100",
        )

    with verdict_column:
        if passed:
            st.success("PASS — Meets the 60% ATS threshold")
        else:
            st.error("FAIL — Below the 60% ATS threshold")

    st.subheader("Executive Summary")
    st.markdown(report["summary"])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Keyword Match")
        st.metric(
            "Keyword Score",
            f"{keyword_match.get('keyword_match_score', 0)}/100",
        )

        present_keywords = [
            item.get("keyword", "")
            for item in keyword_match.get("present", [])
        ]

        missing_keywords = [
            item.get("keyword", "")
            for item in keyword_match.get("missing", [])
        ]

        st.write("**Present keywords:**")
        st.write(", ".join(present_keywords) or "None detected")

        st.write("**Missing keywords:**")
        st.write(", ".join(missing_keywords) or "None detected")

        st.subheader("Bullet Quality")
        st.metric(
            "Bullet Quality Score",
            f"{bullets.get('bullet_quality_avg', 0)}/100",
        )

    with col2:
        st.subheader("Structure")
        st.metric(
            "Structure Score",
            f"{structure.get('structure_score', 0)}/100",
        )

        st.subheader("Terminology")
        st.metric(
            "Jargon Score",
            f"{jargon.get('jargon_score', 0)}/100",
        )

        st.subheader("Background Fit")
        st.metric(
            "Background Fit Score",
            f"{background_fit.get('background_fit_score', 0)}/100",
        )

        st.write(
            background_fit.get(
                "alignment_commentary",
                "No background commentary returned.",
            )
        )

    with st.expander("View complete analysis data"):
        st.json(report)