from google import genai

from config import GEMINI_API_KEY, GEMINI_MODEL


client = genai.Client(api_key=GEMINI_API_KEY)


def analyze_review_sentiment(
    review_content: str,
) -> tuple[str, int, str]:
    prompt = f"""
You are a customer-review sentiment analyzer.

Analyze the review below and provide:

1. A concise summary of the review.
2. A sentiment rating from 1 to 10.

Finish your response using exactly this format:

FINAL_RATING: X

Customer review:
{review_content}
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    raw_output = response.text or ""

    rating = parse_rating(raw_output)
    category = classify_rating(rating)
    clean_summary = remove_rating_line(raw_output)

    return clean_summary, rating, category


def parse_rating(raw_output: str) -> int:
    if "FINAL_RATING:" not in raw_output:
        raise ValueError(
            "Gemini response did not contain FINAL_RATING."
        )

    parts = raw_output.split("FINAL_RATING:", 1)

    rating_text = "".join(
        filter(str.isdigit, parts[1])
    )

    if not rating_text:
        raise ValueError(
            "No valid numeric rating found in Gemini response."
        )

    rating = int(rating_text)

    if rating < 1 or rating > 10:
        raise ValueError(
            f"Rating must be from 1 to 10, received {rating}."
        )

    return rating


def classify_rating(rating: int) -> str:
    if rating >= 7:
        return "Good"

    if rating >= 4:
        return "Average"

    return "Bad"


def remove_rating_line(raw_output: str) -> str:
    summary = raw_output.split("FINAL_RATING:", 1)[0]

    return summary.strip()