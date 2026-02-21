from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QComboBox, QDateEdit, QTabWidget
)
from PyQt5.QtCore import QDate
from expense_manager import add_expense, get_all_expenses, filter_expenses, summary_by_category, total_expenses

class ExpenseTrackerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Tracker")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.init_add_tab()
        self.init_view_tab()
        self.init_filter_tab()
        self.init_summary_tab()

    # ---------------- Add Expense Tab ----------------
    def init_add_tab(self):
        self.add_tab = QWidget()
        layout = QVBoxLayout()

        # Date
        self.date_edit = QDateEdit(calendarPopup=True)
        self.date_edit.setDate(QDate.currentDate())
        layout.addWidget(QLabel("Date:"))
        layout.addWidget(self.date_edit)

        # Amount
        self.amount_input = QLineEdit()
        layout.addWidget(QLabel("Amount:"))
        layout.addWidget(self.amount_input)

        # Category
        self.category_input = QLineEdit()
        layout.addWidget(QLabel("Category:"))
        layout.addWidget(self.category_input)

        # Description
        self.desc_input = QLineEdit()
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.desc_input)

        # Button
        self.add_btn = QPushButton("Add Expense")
        self.add_btn.clicked.connect(self.add_expense_action)
        layout.addWidget(self.add_btn)

        self.add_tab.setLayout(layout)
        self.tabs.addTab(self.add_tab, "Add Expense")

    def add_expense_action(self):
        date = self.date_edit.date().toString("yyyy-MM-dd")
        amount = float(self.amount_input.text())
        category = self.category_input.text()
        description = self.desc_input.text()
        add_expense(date, amount, category, description)
        self.amount_input.clear()
        self.category_input.clear()
        self.desc_input.clear()

    # ---------------- View Expenses Tab ----------------
    def init_view_tab(self):
        self.view_tab = QWidget()
        layout = QVBoxLayout()
        self.expense_table = QTableWidget()
        layout.addWidget(self.expense_table)

        self.load_btn = QPushButton("Load All Expenses")
        self.load_btn.clicked.connect(self.load_expenses)
        layout.addWidget(self.load_btn)

        self.view_tab.setLayout(layout)
        self.tabs.addTab(self.view_tab, "View Expenses")

    def load_expenses(self):
        data = get_all_expenses()
        self.expense_table.setRowCount(len(data))
        self.expense_table.setColumnCount(4)
        self.expense_table.setHorizontalHeaderLabels(["Date", "Amount", "Category", "Description"])
        for i, row in enumerate(data):
            self.expense_table.setItem(i, 0, QTableWidgetItem(row[1]))
            self.expense_table.setItem(i, 1, QTableWidgetItem(f"{row[2]:.2f}"))
            self.expense_table.setItem(i, 2, QTableWidgetItem(row[3]))
            self.expense_table.setItem(i, 3, QTableWidgetItem(row[4]))

    # ---------------- Filter Expenses Tab ----------------
    def init_filter_tab(self):
        self.filter_tab = QWidget()
        layout = QVBoxLayout()

        self.start_date = QDateEdit(calendarPopup=True)
        self.start_date.setDate(QDate.currentDate())
        layout.addWidget(QLabel("Start Date:"))
        layout.addWidget(self.start_date)

        self.end_date = QDateEdit(calendarPopup=True)
        self.end_date.setDate(QDate.currentDate())
        layout.addWidget(QLabel("End Date:"))
        layout.addWidget(self.end_date)

        self.filter_category = QLineEdit()
        layout.addWidget(QLabel("Category (optional):"))
        layout.addWidget(self.filter_category)

        self.filter_btn = QPushButton("Filter")
        self.filter_btn.clicked.connect(self.filter_expenses_action)
        layout.addWidget(self.filter_btn)

        self.filter_table = QTableWidget()
        layout.addWidget(self.filter_table)

        self.filter_tab.setLayout(layout)
        self.tabs.addTab(self.filter_tab, "Filter Expenses")

    def filter_expenses_action(self):
        start = self.start_date.date().toString("yyyy-MM-dd")
        end = self.end_date.date().toString("yyyy-MM-dd")
        category = self.filter_category.text() or None
        data = filter_expenses(start, end, category)
        self.filter_table.setRowCount(len(data))
        self.filter_table.setColumnCount(4)
        self.filter_table.setHorizontalHeaderLabels(["Date", "Amount", "Category", "Description"])
        for i, row in enumerate(data):
            self.filter_table.setItem(i, 0, QTableWidgetItem(row[1]))
            self.filter_table.setItem(i, 1, QTableWidgetItem(f"{row[2]:.2f}"))
            self.filter_table.setItem(i, 2, QTableWidgetItem(row[3]))
            self.filter_table.setItem(i, 3, QTableWidgetItem(row[4]))

    # ---------------- Summary Tab ----------------
    def init_summary_tab(self):
        self.summary_tab = QWidget()
        layout = QVBoxLayout()

        self.summary_btn = QPushButton("Load Summary")
        self.summary_btn.clicked.connect(self.load_summary)
        layout.addWidget(self.summary_btn)

        self.summary_table = QTableWidget()
        layout.addWidget(self.summary_table)

        self.summary_tab.setLayout(layout)
        self.tabs.addTab(self.summary_tab, "Summary")

    def load_summary(self):
        data = summary_by_category()
        total = total_expenses()
        self.summary_table.setRowCount(len(data) + 1)
        self.summary_table.setColumnCount(2)
        self.summary_table.setHorizontalHeaderLabels(["Category", "Amount"])
        for i, (cat, amt) in enumerate(data):
            self.summary_table.setItem(i, 0, QTableWidgetItem(cat))
            self.summary_table.setItem(i, 1, QTableWidgetItem(f"{amt:.2f}"))
        self.summary_table.setItem(len(data), 0, QTableWidgetItem("Total"))
        self.summary_table.setItem(len(data), 1, QTableWidgetItem(f"{total:.2f}"))