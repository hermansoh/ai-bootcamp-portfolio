import streamlit as st

from database.db_manager import (
    get_summaries_by_category,
    init_db,
    save_summary,
)
from services.gemini_service import analyze_review_sentiment


st.set_page_config(
    page_title="Review Analytics",
    page_icon="⭐",
    layout="wide",
)

init_db()

st.title("⭐ Customer Review Analytics")

review_content = st.text_area(
    "Enter a customer review",
    height=200,
)

analyze_button = st.button(
    "Analyze Review",
    type="primary",
)

if analyze_button:
    if not review_content.strip():
        st.error("Please enter a customer review.")
        st.stop()

    try:
        with st.spinner("Analyzing review..."):
            summary, rating, category = (
                analyze_review_sentiment(review_content)
            )

            save_summary(
                review_content,
                summary,
                rating,
                category,
            )

        st.success("Review analyzed successfully.")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Rating", f"{rating}/10")

        with col2:
            st.metric("Category", category)

        st.subheader("Summary")
        st.write(summary)

    except Exception as exc:
        st.error(f"Analysis failed: {exc}")


st.sidebar.header("Review History")

selected_category = st.sidebar.selectbox(
    "Filter by category",
    [
        "All",
        "Good",
        "Average",
        "Bad",
    ],
)

history = get_summaries_by_category(
    selected_category
)

if not history:
    st.sidebar.info("No saved reviews found.")
else:
    for item in history:
        with st.expander(
            f"{item['category']} — "
            f"{item['rating']}/10"
        ):
            st.write(item["summary"])
            st.caption(item["created_at"])