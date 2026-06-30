from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "change_this_secret_key"

DB_CONFIG = {
    "host": "localhost",
    "user": "appuser",
    "password": "apppassword",
    "database": "userdb"
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        city = request.form["city"]
        address = request.form["address"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username,password,email,city,address) VALUES (%s,%s,%s,%s,%s)",
            (username, password, email, city, address)
        )
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            message = "Invalid username or password"

    return render_template("login.html", message=message)

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
