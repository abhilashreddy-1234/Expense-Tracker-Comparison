# Python Expense Tracker

A desktop expense tracker built with **PyQt5** and **SQLite**.

## Features

- Add expenses from a GUI form.
- View all expenses in a table.
- Filter expenses by date range and optional category.
- Show summary totals per category and overall total.

## Tech stack

- Python 3
- PyQt5 (GUI)
- SQLite3 (persistence)

## Project structure

```text
Python-Expense-Tracker/
├── main.py            # App entry point
├── ui_main.py         # GUI tabs and event handlers
├── expense_manager.py # Database CRUD/query helpers
├── init_db.py         # SQLite schema initialization
├── data/
│   └── expenses.db    # SQLite database file
└── expenses.db        # Additional DB file present in repo root of this app
```

## Database

`init_db.py` creates table `expenses` with:

- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `date` (TEXT)
- `category` (TEXT)
- `description` (TEXT)
- `amount` (REAL)

## Setup and run

From this directory:

```bash
python3 -m venv env
source env/bin/activate
pip install PyQt5
python3 init_db.py
python3 main.py
```

If you already have a working environment, the minimal commands are:

```bash
python3 init_db.py
python3 main.py
```

## How the app is organized

- `main.py` launches `ExpenseTrackerUI`.
- `ui_main.py` defines four tabs:
  - **Add Expense**
  - **View Expenses**
  - **Filter Expenses**
  - **Summary**
- `expense_manager.py` handles:
  - inserting expenses,
  - retrieving all expenses,
  - filtered queries,
  - grouped summary and total calculations.

## Important path note

`expense_manager.py` uses `data/expenses.db` as a relative path. Run the app from `Python-Expense-Tracker/` so the database path resolves correctly.

## Known limitations

- No edit/update flow for existing expense rows.
- No delete action in the current Python UI.
- No schema migration/versioning support.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'PyQt5'`**
  - Install with `pip install PyQt5` in your active environment.
- **Database not found / empty state issues**
  - Run `python3 init_db.py` before launching.
