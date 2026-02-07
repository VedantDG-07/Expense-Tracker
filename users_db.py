import sqlite3
from expenses_db import *
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "Backend")
os.makedirs(DB_DIR, exist_ok=True)

USERS_DB = "Backend/users.db"

def get_users_db():
    conn = sqlite3.connect(USERS_DB, timeout=15, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_users_db():
    conn = get_users_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            phone_no TEXT Not NULL,
            password TEXT NOT NULL,
            points INTEGER DEFAULT 0            
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS completed_challenges(
            user_id INTEGER,
            challenge TEXT,
            PRIMARY KEY(user_id, challenge)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS user_limits(
            user_id INTEGER PRIMARY KEY,
            food_limit REAL DEFAULT 0,
            travel_limit REAL DEFAULT 0,
            savings_goal REAL DEFAULT 0,
            weekly_budget REAL DEFAULT 0,
            monthly_budget REAL DEFAULT 0
            )
    """)
    conn.commit()
    conn.close()


init_users_db()
def add_points(user_id, points, conn):
    conn.execute(
        "UPDATE users SET points = points + ? WHERE id = ?",
        (points, user_id)
    )

def set_points(user_id, points):
    conn = get_users_db()
    conn.execute("UPDATE users SET points = ? WHERE id = ?", (points, user_id))
    conn.commit()
    conn.close()

def get_points(user_id):
    conn = get_users_db()
    row = conn.execute("SELECT points FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return row["points"] if row is not None else 0

def returnUser():
    conn=get_users_db()
    conn.execute("SELECT id FROM users")


def check_challenges(user_id):
    conn = get_users_db()

    limits = conn.execute(
        "SELECT * FROM user_limits WHERE user_id=?",
        (user_id,)
    ).fetchone()

    if not limits:
        conn.close()
        return

    food_limit = limits["food_limit"]
    travel_limit = limits["travel_limit"]
    monthly_budget = limits["monthly_budget"]   

    expenses = get_user_expenses(user_id)

    food_total = sum(e["amount"] for e in expenses if e["category"] == "Food")
    travel_total = sum(e["amount"] for e in expenses if e["category"] == "Travel")
    total_expense = sum(e["amount"] for e in expenses)

    done = conn.execute(
        "SELECT challenge FROM completed_challenges WHERE user_id=?",
        (user_id,)
    ).fetchall()
    done = {d["challenge"] for d in done}

    # 🍔 FOOD CONTROL
    if food_total > 0 and food_total <= food_limit and "food_control" not in done:
        add_points(user_id, 5, conn)
        conn.execute(
            "INSERT OR IGNORE INTO completed_challenges VALUES (?,?)",
            (user_id, "food_control")
        )

    # 🚗 TRAVEL SAVER
    if travel_total > 0 and travel_total <= travel_limit and "travel_saver" not in done:
        add_points(user_id, 10, conn)
        conn.execute(
            "INSERT OR IGNORE INTO completed_challenges VALUES (?,?)",
            (user_id, "travel_saver")
        )

    # 💰 MONTHLY BUDGET MASTER
    if total_expense > 0 and total_expense <= monthly_budget and "budget_master" not in done:
        add_points(user_id, 15, conn)
        conn.execute(
            "INSERT OR IGNORE INTO completed_challenges VALUES (?,?)",
            (user_id, "budget_master")
        )

    conn.commit()
    conn.close()

def get_rank(points):
    level = points // 100 + 1
    ranks = {
        1: "Beginner Saver",
        2: "Smart Spender",
        3: "Budget Warrior",
        4: "Finance Ninja",
        5: "Money Master"
    }
    return ranks.get(level, "Legend Saver")

def get_completed_challenges(user_id):
    conn = get_users_db()
    data = conn.execute(
        "SELECT challenge FROM completed_challenges WHERE user_id=?",
        (user_id,)
    ).fetchall()
    conn.close()
    return [d["challenge"] for d in data] if data else []
print("succes")

def get_user_by_email(email):
    conn = get_users_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cur.fetchone()
    conn.close()
    return user


def update_user_password_by_email(email, new_password):
    conn = get_users_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET password=? WHERE email=?", (new_password, email))
    conn.commit()
    conn.close()


    


