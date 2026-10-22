
# Expense Tracker MCP Server

A beginner-friendly Python project that exposes expense-tracking features
through the Model Context Protocol (MCP).

## Features

### Tools
1. `add_expense` - save an expense.
2. `monthly_total` - calculate spending for a month.
3. `top_categories` - rank spending categories for a month.

### Resource
- `expenses://monthly/{month}` - read expense records for a month.

Example resource URI:
`expenses://monthly/2026-10`

### Prompt
- `budget_summary` - prepare a reusable monthly budget-summary prompt.

## Technologies

- Python
- SQLite
- MCP Python SDK
- VS Code
- MCP Inspector

## Project files

- `server.py`: MCP server, database operations, validation, tools,
  resource, and prompt.
- `requirements.txt`: Python dependency.
- `tests/test_expenses.py`: automated unit tests.
- `.vscode/mcp.json`: VS Code MCP connection configuration.
- `expenses.db`: generated automatically on server startup.

## Windows setup

Open the project folder in VS Code.

### 1. Create a virtual environment

Open the VS Code terminal and run:

```powershell
py -m venv .venv
```

If `py` is not recognized, try:

```powershell
python -m venv .venv
```

### 2. Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt in VS Code:

```cmd
.venv\Scripts\activate.bat
```

You can also run the environment's Python directly without activating it.

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If `python` is not found, use the full path:
`.venv\Scripts\python.exe`

### 4. Run the tests

```powershell
python -m unittest discover -s tests -v
```

All four tests should pass before the demo.

### 5. Initialize and run the server

```powershell
python server.py
```

The server runs using standard input/output (stdio), waiting for an MCP client.
Do not type normal commands into this terminal while it is running.
Stop it with Ctrl+C when appropriate.

The database is created automatically beside `server.py`.

## MCP Inspector demo

1. Install Node.js if `npx` is not available.
2. Open a new terminal.
3. Run:

   ```powershell
   npx -y @modelcontextprotocol/inspector
   ```

4. Open the local Inspector URL printed by the command.
5. Choose the STDIO transport.
6. Set the command to the full path to the virtual environment's Python:
   `C:\path\to\expense_tracker_mcp\.venv\Scripts\python.exe`
7. Add the server script path as an argument:
   `C:\path\to\expense_tracker_mcp\server.py`
8. Connect to the server.

### What to demonstrate

- Tools: list the three tools.
- `add_expense`: add a sample expense.
- `monthly_total`: calculate the sample month's total.
- `top_categories`: rank categories.
- Resources: read `expenses://monthly/2026-10`.
- Prompts: select `budget_summary` and provide a month.

Use the exact input parameter names displayed by Inspector.

## Connect to VS Code

1. Open `.vscode/mcp.json`.
2. Replace the example Windows username and project paths.
3. Save the file.
4. Open the VS Code feature or AI extension that supports MCP servers.
5. Reload or restart the MCP connection if necessary.
6. Start `expense-tracker` using that client's MCP controls.
7. Verify that the three tools are available.

VS Code MCP support and UI labels depend on the installed VS Code version and AI extension. If the server does not appear, inspect the MCP output/logs and verify the configured Python and script paths.

## GitHub upload

Create a new empty GitHub repository named `expense-tracker-mcp`.

In the VS Code terminal, run:

```powershell
git init
git add .
git commit -m "Build Expense Tracker MCP server"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/expense-tracker-mcp.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

Make sure `expenses.db`, `.venv`, and personal data are not committed.

## Architecture

- Host: the AI application used by the user.
- Client: the component in the host that communicates with MCP servers.
- Server: this Python application.
- Tools: callable operations for adding and analyzing expenses.
- Resource: readable monthly expense data.
- Prompt: reusable instructions for creating a budget summary.

## Important note

MCP provides the connection between the AI application and this server.
The server itself does not contain an AI model. Natural-language tool selection
depends on the connected host and model.

## Future improvements

- Add expense editing and deletion.
- Add currency formatting.
- Add user authentication.
- Add budget limits and alerts.
