
import sqlite3
DB_PATH = 'data/expenses.db'

def connect_db():
    return sqlite3.connect(DB_PATH)

def add_expense(date, amount, category, description=''):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO expenses (date, amount, category, description) VALUES (?, ?, ?, ?)',
        (date, amount, category, description)
    )
    conn.commit()
    conn.close()

def get_all_expenses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses ORDER BY date ASC')
    rows = cursor.fetchall()
    conn.close()
    return rows

def filter_expenses(start_date=None, end_date=None, category=None):
    conn = connect_db()
    cursor = conn.cursor()
    query = 'SELECT * FROM expenses WHERE 1=1'
    params = []
    if start_date:
        query += ' AND date >= ?'
        params.append(start_date)
    if end_date:
        query += ' AND date <= ?'
        params.append(end_date)
    if category:
        query += ' AND category = ?'
        params.append(category)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

def summary_by_category():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    rows = cursor.fetchall()
    conn.close()
    return rows

def total_expenses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(amount) FROM expenses')
    total = cursor.fetchone()[0] or 0
    conn.close()
    return total
