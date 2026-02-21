# ui_main.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QTabWidget, QDateEdit, QComboBox, QMessageBox
)
from PyQt5.QtCore import QDate
from expense_manager import add_expense, get_all_expenses, filter_expenses, summary_by_category, total_expenses

class ExpenseTrackerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Expense Tracker')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Initialize all tabs
        self.init_add_tab()
        self.init_view_tab()
        self.init_filter_tab()
        self.init_summary_tab()

    # ---------------- Add Expense Tab ----------------
    def init_add_tab(self):
        self.add_tab = QWidget()
        layout = QVBoxLayout()

        self.date_input = QDateEdit(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        layout.addWidget(QLabel("Date:"))
        layout.addWidget(self.date_input)

        self.amount_input = QLineEdit()
        layout.addWidget(QLabel("Amount:"))
        layout.addWidget(self.amount_input)

        self.category_input = QLineEdit()
        layout.addWidget(QLabel("Category:"))
        layout.addWidget(self.category_input)

        self.desc_input = QLineEdit()
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.desc_input)

        self.add_btn = QPushButton("Add Expense")
        self.add_btn.clicked.connect(self.add_expense_clicked)
        layout.addWidget(self.add_btn)

        self.add_tab.setLayout(layout)
        self.tabs.addTab(self.add_tab, "Add Expense")

    def add_expense_clicked(self):
        date = self.date_input.date().toString("yyyy-MM-dd")
        try:
            amount = float(self.amount_input.text())
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Amount must be a number")
            return
        category = self.category_input.text()
        if not category:
            QMessageBox.warning(self, "Input Error", "Category cannot be empty")
            return
        description = self.desc_input.text()

        add_expense(date, amount, category, description)
        self.amount_input.clear()
        self.category_input.clear()
        self.desc_input.clear()
        QMessageBox.information(self, "Success", "Expense added successfully")
        self.update_view_tab()
        self.update_summary_tab()

    # ---------------- View Expenses Tab ----------------
    def init_view_tab(self):
        self.view_tab = QWidget()
        layout = QVBoxLayout()

        self.view_table = QTableWidget()
        self.view_table.setColumnCount(5)
        self.view_table.setHorizontalHeaderLabels(['ID', 'Date', 'Amount', 'Category', 'Description'])
        layout.addWidget(self.view_table)

        self.view_tab.setLayout(layout)
        self.tabs.addTab(self.view_tab, "View Expenses")

        self.update_view_tab()

    def update_view_tab(self):
        expenses = get_all_expenses()
        self.view_table.setRowCount(len(expenses))
        for row_idx, row_data in enumerate(expenses):
            for col_idx, value in enumerate(row_data):
                self.view_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    # ---------------- Filter Expenses Tab ----------------
    def init_filter_tab(self):
        self.filter_tab = QWidget()
        layout = QVBoxLayout()

        self.start_date_input = QDateEdit()
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDate(QDate.currentDate().addMonths(-1))
        layout.addWidget(QLabel("Start Date:"))
        layout.addWidget(self.start_date_input)

        self.end_date_input = QDateEdit()
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDate(QDate.currentDate())
        layout.addWidget(QLabel("End Date:"))
        layout.addWidget(self.end_date_input)

        self.filter_category_input = QLineEdit()
        layout.addWidget(QLabel("Category (optional):"))
        layout.addWidget(self.filter_category_input)

        self.filter_btn = QPushButton("Filter Expenses")
        self.filter_btn.clicked.connect(self.filter_expenses_clicked)
        layout.addWidget(self.filter_btn)

        self.filter_table = QTableWidget()
        self.filter_table.setColumnCount(5)
        self.filter_table.setHorizontalHeaderLabels(['ID', 'Date', 'Amount', 'Category', 'Description'])
        layout.addWidget(self.filter_table)

        self.filter_tab.setLayout(layout)
        self.tabs.addTab(self.filter_tab, "Filter Expenses")

    def filter_expenses_clicked(self):
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        end_date = self.end_date_input.date().toString("yyyy-MM-dd")
        category = self.filter_category_input.text() or None

        filtered = filter_expenses(start_date=start_date, end_date=end_date, category=category)
        self.filter_table.setRowCount(len(filtered))
        for row_idx, row_data in enumerate(filtered):
            for col_idx, value in enumerate(row_data):
                self.filter_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    # ---------------- Summary Tab ----------------
    def init_summary_tab(self):
        self.summary_tab = QWidget()
        layout = QVBoxLayout()

        self.summary_table = QTableWidget()
        self.summary_table.setColumnCount(2)
        self.summary_table.setHorizontalHeaderLabels(['Category', 'Total Amount'])
        layout.addWidget(self.summary_table)

        self.total_label = QLabel()
        layout.addWidget(self.total_label)

        self.summary_tab.setLayout(layout)
        self.tabs.addTab(self.summary_tab, "Summary")

        self.update_summary_tab()

    def update_summary_tab(self):
        summary = summary_by_category()
        self.summary_table.setRowCount(len(summary))
        for row_idx, (category, total) in enumerate(summary):
            self.summary_table.setItem(row_idx, 0, QTableWidgetItem(category))
            self.summary_table.setItem(row_idx, 1, QTableWidgetItem(str(total)))

        total_all = total_expenses()
        self.total_label.setText(f"Total Expenses: {total_all}")