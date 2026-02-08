# 💰 **Expanzo – Smart Expense Tracker with Gamification**

Expanzo is a **Flask-based Expense Tracking Web Application** that helps users manage spending, track budgets, and build better financial habits through **gamified challenges and insights**.

---

## 🚀 Features

### 👤 User System

* User Registration & Login
* Profile Management
* Change Password
* Forgot Password with OTP verification

### 💸 Expense Management

* Add expenses by category
* Add income
* View all transactions
* Search transactions

### 📊 Analytics & Reports

* Category-wise expense summary
* Weekly spending trends
* Visual financial insights

### 🎯 Gamification

* XP-based reward system
* Levels & ranks
* Smart challenges:

  * Food Control
  * Travel Saver
  * Budget Master

### ⚙ Budget Control

* Set food, travel & monthly budget limits
* Auto progress tracking
* Challenge completion detection

### 🔐 Security (Demo Level)

* OTP-based password reset (alert demo)
* Session-based authentication

---

## 🏗 Tech Stack

| Layer    | Technology        |
| -------- | ----------------- |
| Backend  | Python, Flask     |
| Database | SQLite            |
| Frontend | HTML, CSS, Jinja2 |
| Charts   | Chart.js          |
| Auth     | Flask Sessions    |

---

## 📁 Project Structure

```
MVP/
│
├── app.py
├── users_db.py
├── expenses_db.py
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── transactions.html
│   ├── challenges.html
│   ├── settings.html
│   ├── forgot_password.html
│   ├── verify_otp.html
│   ├── reset_password.html
│   ├── chatbot.html
│
├── static/
│   ├── style.css
│   ├── challenges.css
│   ├── settings.css
│   ├── chatbot.css
│
└── Backend/
    ├── users.db
    ├── expenses.db
```

---

## ⚙ Installation

1️⃣ Clone project

```
git clone <repo-url>
cd MVP
```

2️⃣ Install dependencies

```
pip install flask
```

3️⃣ Run app

```
python app.py
```

4️⃣ Open browser

```
http://127.0.0.1:5000
```

---

## 🔁 OTP Password Reset Flow

1. User enters email
2. OTP generated and shown in alert (demo)
3. OTP verified
4. Password reset allowed

---

## 🧠 Future Enhancements

* Email-based OTP
* Password hashing (bcrypt)
* AI chatbot financial assistant
* Split expense module
* Export reports
* Dark/Light mode

---

## 🎓 Academic Use

This project demonstrates:

* Flask Web Development
* Database Integration
* Session Handling
* Form Processing
* Gamification in FinTech
* Full-stack mini project design

---

## 👨‍💻 Author

**Vedant Gawde**
**Mrunmayee Shinde**
**Bhavesh Gambhirrao**

---

## 📜 License

This project is for educational and demonstration purposes.

---

