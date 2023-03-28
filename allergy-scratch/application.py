import os
import sys
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///allergy.db")
db.execute("CREATE TABLE IF NOT EXISTS allergy (user_id INTEGER, symbol TEXT, date TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, confirmation TEXT, firstname TEXT, lastname TEXT, account TEXT)")
# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")

def portfolio(user_id):
    rows = db.execute("SELECT * FROM allergy WHERE user_id = ?", session["user_id"])
    user_rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    food_list = []
    firstname = user_rows[0]['firstname']
    lastname = user_rows[0]['lastname']
    rows = db.execute("SELECT * FROM allergy WHERE user_id = ?", session["user_id"])
    for row in rows:
        food_symbol = row['symbol']
        date = row['date']
        if food_symbol not in food_list:
            food_list.append([food_symbol, date])

    return food_list, firstname, lastname

@app.route("/")
@login_required
def index():
    food_portfolio, firstname, lastname = portfolio(session["user_id"])
    return render_template("index.html", food_portfolio=food_portfolio, firstname=firstname, lastname=lastname)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Must provide Allergy Item", 403)
        rows = db.execute("SELECT * FROM allergy WHERE user_id = ? AND symbol = ?", session["user_id"], request.form.get("symbol"))
        if len(rows) != 0:
            db.execute("DELETE FROM allergy WHERE user_id = ? AND symbol = ?", session["user_id"], request.form.get("symbol"))
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        db.execute("INSERT INTO allergy (user_id, symbol, date) VALUES(?, ?, ?)", session["user_id"], request.form.get("symbol"), dt_string)

        return redirect("/")
    else:
        return render_template("add.html")

@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():
    if request.method == "POST":
        # Ensure allergy item was submitted
        if not request.form.get("symbol"):
            return apology("must provide Allergy Item", 403)

        # Check if duplicate
        rows = db.execute("SELECT * FROM allergy WHERE user_id = ? AND symbol = ?", session["user_id"], request.form.get("symbol"))

        # Ensure username does not exist
        if len(rows) != 0:
            db.execute("DELETE FROM allergy WHERE user_id = ? AND symbol = ?", session["user_id"], request.form.get("symbol"))
        else:
            return apology("Allergy Item Does Not Exist", 403)

        return redirect("/")

    else:
        return render_template("remove.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        
        elif not request.form.get("password"):
            return apology("must provide password", 403) 
        
        elif not request.form.get("confirmation"):
            return apology("must re-enter password", 403)
        
        elif not request.form.get("firstname"):
            return apology("must provide first name", 403)
        
        elif not request.form.get("lastname"):
            return apology("must provide last name", 403)
        
        elif not request.form.get("account"):
            return apology("must provide account number", 403)

        elif (request.form.get("password") != request.form.get("confirmation")):
            return apology("The passwords don't match", 403)  

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 0:
            return apology("User already exist", 403)       
        
        rows = db.execute("SELECT * FROM users WHERE account = ?", request.form.get("account"))
        
        if len(rows) != 0:
            return apology("Account Number already exist", 403)

        db.execute("INSERT INTO users (username, hash, firstname, lastname, account) VALUES(?, ?, ?, ?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")), request.form.get("firstname"), request.form.get("lastname"), request.form.get("account"))

        return redirect("/")
    else:
        return render_template("register.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)