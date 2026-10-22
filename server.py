
import json

from mcp.server.fastmcp import FastMCP

import expense_db


mcp = FastMCP("Expense Tracker MCP")

# Ensure the database table exists when the server starts.
expense_db.initialize_database()


@mcp.tool()
def add_expense(
    description: str,
    amount: float,
    category: str = "Other",
) -> dict:
    """Record an expense. Amount must be positive."""
    return expense_db.add_expense(description, amount, category)


@mcp.tool()
def list_expenses(limit: int = 100) -> list[dict]:
    """List recent expenses, up to 500 records."""
    return expense_db.list_expenses(limit)


@mcp.tool()
def delete_expense(expense_id: int) -> str:
    """Delete an expense by its ID."""
    deleted = expense_db.delete_expense(expense_id)

    if deleted:
        return f"Expense {expense_id} deleted successfully."

    return f"No expense found with ID {expense_id}."


@mcp.tool()
def get_expense_summary() -> dict:
    """Get the expense count, total spending, and average expense."""
    return expense_db.get_expense_summary()


@mcp.resource("expenses://all")
def expenses_resource() -> str:
    """Read the latest expense records as JSON."""
    records = expense_db.list_expenses(limit=500)
    return json.dumps(records, indent=2, ensure_ascii=False)


@mcp.prompt()
def analyze_spending(month: str = "this month") -> str:
    """Create a prompt for analyzing expense records."""
    return (
        f"Analyze my expense records for {month}. "
        "Summarize total spending, spending by category, "
        "the largest expenses, and practical ways to budget. "
        "Use only the expense records provided to you. "
        "If a date range cannot be determined, state that limitation."
    )


if __name__ == "__main__":
    # STDIO is the local transport used in this setup.
    mcp.run(transport="stdio")
