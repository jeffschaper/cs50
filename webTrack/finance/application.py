import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
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

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# 4
@app.route("/")
# main page of website after logging in
# decorator
@login_required
def index():
    """Show portfolio of stocks"""
    return apology("TODO")

# 3
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
       return render_template("buy.html")
    # else:



# 6
@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")

# GET is used when requesting a webpage
# POST is used when submit data via form
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    # if user if trying to login and already has an account
    if request.method == "POST":

        # Ensure username was submitted
        # request.form is the data the user submitted
        # get input field
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        # connect 'controller' (applicaiton.py) to 'model' (database)
        # : is placeholder
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                            # take the form, get the username
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        # if len is 0, then it doesn't exist assuming usernames are unique
        # passwords are hashed instead of storing literal string
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        # get the value of id column of the first row
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    # If user just wants to GET the login page before POSTing the login information
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# 2
@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    # POST
    else:
        sym = request.form.get("symbol")
        Look = lookup(sym)
        if Look is None:
            return apology("symbol does not exist")
    return render_template("quoted.html", result=Look)


# 1
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # if the user clicks on the registration link, direct them to the registration page (register.html)
    if request.method == "GET":
        return render_template("register.html")

    # when the user clicks 'register'
    if request.method == "POST":
        # error checking
        # username is blank or password is blank
        if request.form.get("username") == '' or request.form.get("password") == '':
            return apology("username and password must be provided", 403)

        # username already exists
        # check database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                            # take the form, get the username
                          username=request.form.get("username"))

        # if a username exists
        if len(rows) == 1:
            return apology("username already exists", 403)

        # passwords do not match
        if request.form.get("password") != request.form.get("passwordAgain"):
            return apology("passwords do not match", 403)

        # if inputs match all the error checks
        else:
            # hash password
            passHash = generate_password_hash(request.form.get("password"))
            # insert into table
            insert = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                                username=request.form.get("username"),hash=passHash)
        return render_template("/")

# 5
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")

# 7 (personal touch)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)