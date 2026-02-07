import sqlite3
from datetime import datetime
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "Backend")
os.makedirs(DB_DIR, exist_ok=True)

EXPENSES_DB = "Backend/expenses.db"

def get_expenses_db():
    conn = sqlite3.connect(EXPENSES_DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_expenses_db():
    conn = get_expenses_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            expense_date TEXT NOT NULL,
            entry_date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS no_spend_days (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            UNIQUE(user_id, date)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            income_date TEXT,
            amount REAL,
            category TEXT
        )
    """)
    
    conn.commit()
    conn.close()


def add_expense(user_id, expense_date, category, amount):
    conn = get_expenses_db()
    entry_date = datetime.today().strftime("%Y-%m-%d")

    conn.execute("""
        INSERT INTO expenses (user_id, expense_date, entry_date, category, amount)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, expense_date, entry_date, category, float(amount)))

    conn.commit()
    conn.close()

def add_income(user_id,income_date,category, amount):
    conn = get_expenses_db()
    conn.execute("""
        INSERT INTO income (user_id,income_date, category, amount)
        VALUES (?, ?, ?, ?)
    """, (user_id,income_date,category,float(amount)))
    conn.commit()
    conn.close()

def get_user_income(user_id):
    conn = get_expenses_db()
    data = conn.execute("""
        SELECT id, income_date, category, amount
        FROM income
        WHERE user_id=?
        ORDER BY income_date DESC
    """, (user_id,)).fetchall()
    conn.close()
    return data or []

def get_user_expenses(user_id):
    conn = get_expenses_db()
    data = conn.execute("""
        SELECT id, expense_date, entry_date, category, amount
        FROM expenses
        WHERE user_id=?
        ORDER BY expense_date DESC
    """, (user_id,)).fetchall()
    conn.close()
    return data or []

def get_recent_transactions(user_id):
    conn = get_expenses_db()

    data = conn.execute("""
        SELECT expense_date AS date, category, amount, 'expense' AS type
        FROM expenses
        WHERE user_id=?

        ORDER BY date DESC
        LIMIT 5
    """, (user_id,)).fetchall()
        # UNION ALL

        # SELECT income_date AS date, category, amount, 'income' AS type
        # FROM income
        # WHERE user_id=?
    conn.close()
    return data or []

def add_no_spend_day(user_id):
    conn = get_expenses_db()
    today = datetime.today().strftime("%Y-%m-%d")

    conn.execute("""
        INSERT OR IGNORE INTO no_spend_days (user_id, date)
        VALUES (?, ?)
    """, (user_id, today))

    conn.commit()
    conn.close()

def search_expenses(user_id, keyword):
    if not keyword:       
        return []
    
    keyword = keyword.strip()

    conn = get_expenses_db()

    results = conn.execute("""
        SELECT id, expense_date, entry_date, category, amount
        FROM expenses
        WHERE user_id=?
        AND (LOWER(category) LIKE LOWER(?) OR expense_date LIKE ?)
        ORDER BY entry_date DESC
    """, (user_id, f"%{keyword}%", f"%{keyword}%")).fetchall()

    conn.close()
    return results


def get_no_spend_days(user_id):
    conn = get_expenses_db()
    data = conn.execute(
        "SELECT date FROM no_spend_days WHERE user_id=?",
        (user_id,)
    ).fetchall()
    conn.close()
    return [d["date"] for d in data] if data else []


def get_category_wise_expense(user_id):
    conn = get_expenses_db()
    data = conn.execute("""
        SELECT category, SUM(amount) AS total
        FROM expenses
        WHERE user_id = ?
        GROUP BY category
    """, (user_id,)).fetchall()
    conn.close()
    return data