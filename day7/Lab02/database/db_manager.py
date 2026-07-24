import sqlite3
from datetime import datetime

from config import DB_NAME


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS review_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                review_content TEXT NOT NULL,
                summary TEXT NOT NULL,
                rating INTEGER NOT NULL,
                category TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        connection.commit()


def save_summary(
    review_content: str,
    summary: str,
    rating: int,
    category: str,
) -> None:
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO review_summaries (
                review_content,
                summary,
                rating,
                category,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                review_content,
                summary,
                rating,
                category,
                datetime.now().isoformat(timespec="seconds"),
            ),
        )

        connection.commit()


def get_summaries_by_category(category: str):
    with get_connection() as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        if category == "All":
            cursor.execute(
                """
                SELECT *
                FROM review_summaries
                ORDER BY id DESC
                """
            )
        else:
            cursor.execute(
                """
                SELECT *
                FROM review_summaries
                WHERE category = ?
                ORDER BY id DESC
                """,
                (category,),
            )

        return [dict(row) for row in cursor.fetchall()]


def get_summary_by_id(summary_id: int):
    with get_connection() as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM review_summaries
            WHERE id = ?
            """,
            (summary_id,),
        )

        row = cursor.fetchone()

        return dict(row) if row else None