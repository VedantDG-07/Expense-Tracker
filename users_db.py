import sqlite3


USERS_DB = "Backend/users.db"

def get_users_db():
    conn = sqlite3.connect(USERS_DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_users_db():
    conn = get_users_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            points INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def add_points(user_id, points):
    conn = get_users_db()
    conn.execute("UPDATE users SET points = points + ? WHERE id = ?", (points, user_id))
    conn.commit()
    conn.close()

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


init_users_db()
print("succes")