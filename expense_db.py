
import sqlite3
from pathlib import Path
from typing import Any

# Store the database beside this Python file.
DB_PATH = Path(__file__).resolve().parent / "expenses.db"


def get_connection(db_path: str | Path | None = None):
    path = Path(db_path) if db_path else DB_PATH
    conn = sqlite3.connect(str(path), timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database(db_path: str | Path | None = None) -> None:
    with get_connection(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                category TEXT NOT NULL DEFAULT 'Other',
                expense_date TEXT NOT NULL DEFAULT
                    (date('now', 'localtime'))
            )
        """)


def add_expense(
    description: str,
    amount: float,
    category: str = "Other",
    db_path: str | Path | None = None,
) -> dict[str, Any]:
    description = description.strip()
    category = category.strip() or "Other"

    if not description:
        raise ValueError("Description cannot be empty.")
    if not isinstance(amount, (int, float)) or isinstance(amount, bool):
        raise ValueError("Amount must be a number.")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    if not category:
        category = "Other"

    with get_connection(db_path) as conn:
        cursor = conn.execute(
            """
            INSERT INTO expenses (description, amount, category)
            VALUES (?, ?, ?)
            """,
            (description, round(float(amount), 2), category),
        )
        row = conn.execute(
            "SELECT * FROM expenses WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()

    return dict(row)


def list_expenses(
    limit: int = 100,
    db_path: str | Path | None = None,
) -> list[dict[str, Any]]:
    if not isinstance(limit, int) or isinstance(limit, bool):
        raise ValueError("Limit must be an integer.")
    if not 1 <= limit <= 500:
        raise ValueError("Limit must be between 1 and 500.")

    with get_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT id, description, amount, category, expense_date
            FROM expenses
            ORDER BY expense_date DESC, id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]


def delete_expense(
    expense_id: int,
    db_path: str | Path | None = None,
) -> bool:
    if not isinstance(expense_id, int) or isinstance(expense_id, bool):
        raise ValueError("Expense ID must be an integer.")
    if expense_id <= 0:
        raise ValueError("Expense ID must be positive.")

    with get_connection(db_path) as conn:
        cursor = conn.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,),
        )
        return cursor.rowcount > 0


def get_expense_summary(
    db_path: str | Path | None = None,
) -> dict[str, Any]:
    with get_connection(db_path) as conn:
        row = conn.execute("""
            SELECT
                COUNT(*) AS expense_count,
                COALESCE(SUM(amount), 0) AS total_amount,
                COALESCE(AVG(amount), 0) AS average_amount
            FROM expenses
        """).fetchone()

    return {
        "expense_count": row["expense_count"],
        "total_amount": round(row["total_amount"], 2),
        "average_amount": round(row["average_amount"], 2),
    }
