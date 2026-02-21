# C++ Expense Tracker (Win32)

A Windows desktop expense tracker implemented in **C++** using the **Win32 API**, with CSV file storage.

## Features

- Add expenses (date, amount, category, description).
- Delete selected expenses.
- Save/load expenses to/from CSV.
- Filter by category.
- Filter by date range (`MM-DD-YYYY`).
- Display running total for visible expenses.

## Tech stack

- C++
- Win32 API (`windows.h`)
- STL (`vector`, `string`, `fstream`, `sstream`, `iomanip`)

## Files

```text
CPP-Expense-Tracker/
├── final_expense_tracker_ui.cpp  # Full Win32 GUI implementation
├── expenses.csv                  # Persistence file
└── ExpenseTracker.exe            # Compiled binary (if present)
```

## Build and run (Windows)

Using MinGW g++:

```bash
g++ final_expense_tracker_ui.cpp -o ExpenseTracker.exe -mwindows
ExpenseTracker.exe
```

## CSV format

The app writes to `expenses.csv` with header:

```csv
Date,Amount,Category,Description
02-20-2026,25.50,Food,Lunch
02-21-2026,120.00,Shopping,Shoes
```

## UI behavior summary

- **Add** inserts a new expense into memory and updates the CSV.
- **Delete** removes selected list item, then persists updated data.
- **Save** writes in-memory records to CSV.
- **Load** replaces in-memory data with CSV contents.
- **Apply Filter** filters by exact category match.
- **Date Filter** validates date format and filters inclusively.
- **Show All** resets list to all loaded expenses.

## Date handling

Date filtering expects `MM-DD-YYYY`. Invalid format is rejected and prompts an error message.

## Known limitations

- Category filter is exact-match (case-sensitive).
- CSV parsing is simple and not quote-aware for commas in description fields.
- Application target is Windows only due to Win32 API dependency.
