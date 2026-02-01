from flask import Flask, render_template, request, redirect, session, url_for, flash
from users_db import get_users_db, init_users_db
from expenses_db import *
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "secret_key"

init_users_db()
init_expenses_db()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db = get_users_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("dashboard"))

        flash("Invalid credentials", "danger")

    return render_template("login.html")

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        passwordp = request.form.get('passwordp')
        passwordc = request.form.get('passwordc')

        if passwordp != passwordc:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register'))

        db = get_users_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                "INSERT INTO users(username,password) VALUES (?,?)",
                (username, passwordp)
            )
            db.commit()
            flash('Account created! Please login.', 'success')
            return redirect(url_for('login'))

        except:
            flash("Username already exists!", "danger")
            return redirect(url_for('register'))

        finally:
            cursor.close()
            db.close()

    return render_template('register.html')

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    expenses = get_user_expenses(user_id)
    no_spend_days = get_no_spend_days(user_id)

    total_expense = sum(e["amount"] for e in expenses)

    activity_dates = set(e["entry_date"] for e in expenses) | set(no_spend_days)

    streak = 0
    today = datetime.today().date()
    today_str = today.strftime("%Y-%m-%d")

    if today_str in activity_dates:
        while True:
            check_day = today - timedelta(days=streak)
            if check_day.strftime("%Y-%m-%d") in activity_dates:
                streak += 1
            else:
                break

    already_marked = today_str in no_spend_days

    return render_template(
        "dashboard.html",
        expenses=expenses,
        total_expense=total_expense,
        streak=streak,
        already_marked=already_marked
    )


@app.route("/add_expense", methods=["POST"])
def add_expense_route():
    if "user_id" not in session:
        return redirect(url_for("login"))

    expense_date = request.form.get("date")
    category = request.form.get("category")
    amount = request.form.get("amount")

    add_expense(session["user_id"], expense_date, category, amount)
    return redirect(url_for("dashboard"))

@app.route("/add_income", methods=["POST"])
def add_income_route():
    if "user_id" not in session:
        return redirect(url_for("login"))

    income_date = request.form.get("date")
    amount = request.form.get("amount")
    source = request.form.get("source")

    add_income(session["user_id"], income_date, amount, source)
    return redirect(url_for("dashboard"))


@app.route("/no_spend_day", methods=["POST"])
def mark_no_spend():
    if "user_id" not in session:
        return redirect(url_for("login"))

    print("NO SPEND CLICKED") 
    add_no_spend_day(session["user_id"])
    flash("No Spend Day recorded", "success")
    return redirect(url_for("dashboard"))


@app.route("/transactions", methods=["GET","POST"])
def transactions():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user_id = session["user_id"]
    conn = get_expenses_db()
    data = conn.execute("""
        SELECT id, expense_date, entry_date, category, amount
        FROM expenses
        WHERE user_id=?
        ORDER BY expense_date ASC
    """, (user_id,)).fetchall()
    conn.close()

    return render_template("transactions.html",expenses=data)

@app.route("/Report_Analysis",methods=["GET","POST"])
def Report_Analysis():
    return render_template("Report_Analysis.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
