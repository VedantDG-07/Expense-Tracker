from flask import Flask, render_template, request, redirect, session, url_for, flash
from users_db import *
from expenses_db import *
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "secret_key"

init_users_db()
init_expenses_db()
expenses=[]
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

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        user = get_user_by_email(email)

        if user:
            import random
            otp = random.randint(100000, 999999)
            session["otp"] = str(otp)
            session["reset_email"] = email

            return render_template("verify_otp.html", otp=otp)

        else:
            return "<script>alert('Email not registered');</script>"

    return render_template("forgot_password.html")

@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    if request.form["otp"] == session.get("otp"):
        return redirect("/reset_password")
    else:
       return "<script>alert('Invalid OTP'); window.location='/forgot-password';</script>"



@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if "reset_email" not in session:
        return redirect("/login")

    if request.method == "POST":
        new_password = request.form["password"]
        update_user_password_by_email(session["reset_email"], new_password)
        session.pop("reset_email")
        return redirect("/login")

    return render_template("reset_password.html")

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        passwordp = request.form.get('passwordp')
        passwordc = request.form.get('passwordc')
        email = request.form.get('email')
        phone = request.form.get('phone')

        if passwordp != passwordc:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register'))

        db = get_users_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                "INSERT INTO users(username,password,email,phone_no) VALUES (?,?,?,?)",
                (username, passwordp,email,phone)
            )
            db.commit()
            flash('Account created! Please login.', 'success')
            return redirect(url_for('login'))

        except sqlite3.IntegrityError:
            flash("Username already exists!", "danger")
        except Exception as e:
            print("REGISTER ERROR:", e)
            flash("Something went wrong", "danger")
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
    income=get_user_income(user_id)
    no_spend_days = get_no_spend_days(user_id)

    total_expense = sum(e["amount"] for e in expenses)
    total_income = sum(i["amount"] for i in income)


    activity_dates = set(e["expense_date"] for e in expenses) | set(no_spend_days)


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


    transactions = get_recent_transactions(user_id)

    return render_template(
        "dashboard.html",
        expenses=expenses,
        total_expense=total_expense,
        streak=streak,
        already_marked=already_marked,
        income=income,
        total_income=total_income,
        transactions=transactions
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
    category = request.form.get("category")

    add_income(session["user_id"], income_date, category, amount)
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
    data = get_user_expenses(user_id)
    return render_template("transactions.html",expenses=data)

@app.route("/search", methods=["GET","POST"])
def search():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user_id = session["user_id"]
    keyword = request.form.get("search")
    
    if keyword!="All":
        results = search_expenses(session["user_id"], keyword)
    else:
        results=get_user_expenses(user_id)

    return render_template("transactions.html", expenses=results)



@app.route("/Report_Analysis", methods=["GET", "POST"])
def Report_Analysis():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    conn = get_expenses_db()

    # Category totals
    data = conn.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE user_id=?
        GROUP BY category
    """, (user_id,)).fetchall()

    labels = [d["category"] for d in data]
    values = [d["total"] for d in data]

    # Weekly data
    week_data = conn.execute("""
        SELECT expense_date, SUM(amount)
        FROM expenses
        WHERE user_id=?
        GROUP BY expense_date
        ORDER BY expense_date DESC
        LIMIT 7
    """, (user_id,)).fetchall()

    week_labels = [d[0] for d in week_data][::-1]
    week_values = [d[1] for d in week_data][::-1]

    conn.close()

    return render_template(
        "Report_Analysis.html",
        labels=labels,
        values=values,
        week_labels=week_labels,
        week_values=week_values
    )

@app.route("/settings")
def settings():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_users_db()
    user = conn.execute(
        "SELECT username, email, phone_no FROM users WHERE id=?",
        (session["user_id"],)
    ).fetchone()
    conn.close()

    return render_template("settings.html", user=user)

@app.route("/challenges")
def challenges():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    check_challenges(user_id)
    conn = get_users_db()

    limits = conn.execute(
    "SELECT * FROM user_limits WHERE user_id=?",
    (user_id,)).fetchone()
    conn.close()

    expenses = get_user_expenses(user_id)
    income = get_user_income(user_id)

    food_total = sum(e["amount"] for e in expenses if e["category"] == "Food")
    travel_total = sum(e["amount"] for e in expenses if e["category"] == "Travel")
    total_expense = sum(e["amount"] for e in expenses)
    total_income = sum(i["amount"] for i in income)

    progress = {
        "food": int((food_total / limits["food_limit"]) * 100) if limits and limits["food_limit"] else 0,
        "travel": int((travel_total / limits["travel_limit"]) * 100) if limits and limits["travel_limit"] else 0,
        "budget": int((total_expense / limits["monthly_budget"]) * 100) if limits and limits["monthly_budget"] else 0
    }


    points = get_points(user_id)
    level = points // 100 + 1
    rank = get_rank(points)
    done_challenges = get_completed_challenges(user_id)

    return render_template(
        "challenges.html",
        limits=limits,
        progress=progress,
        points=points,
        level=level,
        rank=rank,
        done_challenges=done_challenges
    )



@app.route("/set_limits", methods=["POST"])
def set_limits():
    if "user_id" not in session:
        return redirect(url_for("login"))

    food = request.form.get("food_limit")
    travel = request.form.get("travel_limit")
    monthly = request.form.get("monthly_budget")   

    conn = get_users_db()
    conn.execute("""
        INSERT OR REPLACE INTO user_limits
        (user_id, food_limit, travel_limit, monthly_budget)
        VALUES (?,?,?,?)
    """, (session["user_id"], food, travel, monthly))  
    conn.commit()
    conn.close()

    flash("Limits Updated!", "success")
    return redirect(url_for("challenges"))

@app.route("/update_profile", methods=["POST"])
def update_profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    email = request.form.get("email")
    phone = request.form.get("phone")

    conn = get_users_db()
    conn.execute("""
        UPDATE users
        SET email=?, phone_no=?
        WHERE id=?
    """, (email, phone, session["user_id"]))
    conn.commit()
    conn.close()

    flash("Profile updated!", "success")
    return redirect(url_for("settings"))

@app.route("/update_password", methods=["POST"])
def update_password():
    if "user_id" not in session:
        return redirect(url_for("login"))

    current = request.form.get("current_password")
    new = request.form.get("new_password")

    conn = get_users_db()
    user = conn.execute(
        "SELECT password FROM users WHERE id=?",
        (session["user_id"],)
    ).fetchone()

    if user["password"] != current:
        flash("Current password incorrect", "danger")
        conn.close()
        return redirect(url_for("settings"))

    conn.execute(
        "UPDATE users SET password=? WHERE id=?",
        (new, session["user_id"])
    )
    conn.commit()
    conn.close()

    flash("Password updated!", "success")
    return redirect(url_for("settings"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/features")
def features():
    return render_template("features.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
