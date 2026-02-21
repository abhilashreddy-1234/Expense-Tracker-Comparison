# Expense App (Python + C++)

This repository contains **two implementations of an expense tracker**:
- A **Python desktop app** using **PyQt5** with **SQLite** persistence.
- A **C++ desktop app** using the **Win32 API** with **CSV** persistence.

The project is useful for comparing how the same problem domain (expense tracking) is handled across two different language ecosystems.

## Repository layout

```text
Expense-App/
├── Python-Expense-Tracker/
│   ├── main.py
│   ├── ui_main.py
│   ├── expense_manager.py
│   ├── init_db.py
│   └── data/expenses.db
├── CPP-Expense-Tracker/
│   ├── final_expense_tracker_ui.cpp
│   └── expenses.csv
└── README.md
```

## What each app provides

Both apps support core expense-tracking tasks:

- Adding expenses with date, amount, category, and description.
- Viewing saved expenses.
- Filtering expenses.
- Showing totals.

## Implementation differences at a glance

| Area | Python app | C++ app |
|------|------------|---------|
| UI framework | PyQt5 | Win32 API |
| Storage | SQLite database (`data/expenses.db`) | CSV file (`expenses.csv`) |
| Primary file(s) | `ui_main.py`, `expense_manager.py` | `final_expense_tracker_ui.cpp` |
| Runtime target | Cross-platform where PyQt5 is supported | Windows desktop |

## Quick start

### Python app

```bash
cd Python-Expense-Tracker
python3 init_db.py
python3 main.py
```

See app-specific documentation: `Python-Expense-Tracker/README.md`

### C++ app (Windows)

```bash
cd CPP-Expense-Tracker
g++ final_expense_tracker_ui.cpp -o ExpenseTracker.exe -mwindows
ExpenseTracker.exe
```

See app-specific documentation: `CPP-Expense-Tracker/README.md`

## Running the C++ App on macOS (Wine)

The C++ expense tracker is built on the Win32 API, so it is designed for Windows and is not natively compatible with macOS.

You can still run it on macOS by using **Wine**, which acts as a compatibility layer for Windows applications without requiring a full virtual machine.

**Install Wine (Homebrew)**

```bash
brew install --cask wine-stable
```

**Build the executable (if needed)**

```bash
cd CPP-Expense-Tracker
g++ final_expense_tracker_ui.cpp -o ExpenseTracker.exe -mwindows
```

**Run with Wine**

```bash
wine ExpenseTracker.exe
```
