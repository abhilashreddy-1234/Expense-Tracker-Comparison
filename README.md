# Expense-Tracker-Comparison
This project implements an Expense Tracker application in two different programming languages:

Python

C++

Both implementations provide the same core functionality and are designed to demonstrate differences in syntax, structure, and language-specific features.

Expense-Tracker-Comparison
C++ Expense Tracker (Win32 GUI)

This project includes a C++ implementation of an Expense Tracker application built using the Win32 API.

The application provides a graphical user interface to manage daily expenses and store them in a CSV file.

Features

Add new expenses

Delete selected expenses

Save expenses to CSV file

Load expenses from CSV file

Filter by category

Filter by date range (MM-DD-YYYY format)

Automatically calculate and display total expenses

Technologies Used

C++

Win32 API

STL (vector, string, fstream, stringstream)

MinGW g++ compiler

How to Build

Compile using:

g++ final_expense_tracker_ui.cpp -o ExpenseTracker.exe -mwindows

Run:

ExpenseTracker.exe
CSV Format

Expenses are stored in:

expenses.csv

Format:

Date,Amount,Category,Description
02-20-2026,25.50,Food,Lunch
02-21-2026,120.00,Shopping,Shoes

The CSV file updates automatically when adding or deleting expenses.
