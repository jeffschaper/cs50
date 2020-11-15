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
# main page of website after logging in
@app.route("/")
# decorator
@login_required
def index():
    """Show portfolio of stocks"""

    # get who is currently logged in
    user = session["user_id"]

    stocks = db.execute("SELECT A.symbol,A.purchased - ifnull(A.sold,0) AS numberOfShares FROM(\
                        SELECT t.userId, t.symbol, SUM(t.shares) AS purchased,t1.sold FROM Transactions t\
                        LEFT JOIN (SELECT t1.userId,t1.symbol,SUM(t1.shares) AS sold FROM Transactions t1\
                        WHERE t1.userId = :user AND t1.action = 'S'GROUP BY t1.userId, t1.symbol ) t1 ON t1.userId = t.userId\
                        AND t1.symbol = t.symbol WHERE t.userId = :user AND t.action = 'P'GROUP BY t.userId,t.symbol,t1.sold )A\
                        WHERE  A.purchased- ifnull(A.sold,0) > 0",
                        user=user)

    userCash = db.execute("SELECT cash FROM users WHERE id = :user",
                    user=user)

    cash = float(userCash[0]["cash"])

    # print(symbolShares)
    # print(type(symbolShares))
    # sql query returns a list

    # create a new python list
    transactionDetail = []

    # placeholder for total assets
    stockAssets = 0

    # loop through the transactionDetail to get information
    for stock in stocks:
        stockInfo = lookup(stock["symbol"])
        symbol = stock["symbol"]
        stockName = stockInfo["name"]
        shares = stock["numberOfShares"]
        price = float(stockInfo["price"])
        total = round(shares * price,2)
        stockAssets += total

        transactionDetail.append({'symbol':symbol, 'name':stockName, 'shares':shares, 'price':price, 'total':total})

    grandTotal = round(stockAssets + cash,2)
    print(transactionDetail)

    # render index.html (obviously)
    # stocks in html = transactionDetail data
    return render_template("index.html",stocks=transactionDetail, cash=cash, grandTotal=grandTotal)

# 3
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    # POST Method
    else:
        # calculate amount of stocks being purchased
        sym = request.form.get("symbol")
        Look = lookup(sym)
        price = Look["price"]
        shares = request.form.get("shares")

        priceInt = float(price)
        sharesInt = float(shares)

        mult = round((priceInt * sharesInt),2)

        # get session userid
        user = session["user_id"]

        # check users table to ensure user has enough $
        currentCash = db.execute("SELECT cash FROM users WHERE id = :user",
                                user=user)

        currentCashInt = int(currentCash[0]["cash"])

        if currentCashInt > mult or currentCashInt == mult:
            # update users table
            updateUser = db.execute("UPDATE users SET cash = :cash WHERE id = :user",
                                        cash=currentCashInt-mult, user=user)

            # insert record into transaction table
            insert = db.execute("INSERT INTO transactions(userid,symbol,shares,price,action) VALUES(:userid,:symbol,:shares,:price,:action)",
                                                        userid=user, symbol=sym, shares=sharesInt, price=priceInt, action='P')

        else:
            return apology("Sorry, you do not have enough cash to make this purchase")

        # Redirect user to login form
        return redirect("/")

# 6
@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
     # get who is currently logged in
    user = session["user_id"]

    stocks = db.execute("SELECT t.symbol, CASE WHEN t.action = 'S' THEN t.shares * -1 ELSE t.shares END AS numberOfShares, t.price, t.time FROM Transactions t WHERE t.userId = :user",
                        user=user)

    # create a new python list
    transactionHistory = []

    # loop through the transactionDetail to get information
    for stock in stocks:
        symbol = stock["symbol"]
        shares = stock["numberOfShares"]
        price = stock["price"]
        time = stock["time"]

        transactionHistory.append({'symbol':symbol, 'shares':shares, 'price':price, 'time':time})

    return render_template("history.html",stocks=transactionHistory)


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
            return render_template("login.html")

# 5
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        # get current users stocks
        getUserId = session["user_id"]

        # query database
        # error check to only return current stocks
        stocks = db.execute("SELECT A.symbol, A.purchased- ifnull(A.sold,0) as remaining FROM(\
                            SELECT t.userId, t.symbol, SUM(t.shares) AS purchased, t1.sold FROM Transactions t\
                            left JOIN (SELECT t1.userId, t1.symbol, SUM(t1.shares) AS sold FROM Transactions t1\
                            WHERE t1.userId = :userId AND t1.action = 'S' GROUP BY t1.userId, t1.symbol ) t1 ON t1.userId = t.userId\
                            and t1.symbol = t.symbol WHERE t.userId = :userId AND t.action = 'P' GROUP BY t.userId,t.symbol,t1.sold )A\
                            where  A.purchased- ifnull(A.sold,0) > 0;",
                            userId=getUserId)

        print(stocks)

        # create a new python list
        stockList = []

        # loop through the users stocks and display what's currently owned
        for stock in stocks:
            symbol = stock["symbol"]
            stockList.append({'symbol':symbol})

        return render_template("sell.html", stocks=stockList)
    # POST Method
    else:
        # calculate amount of stocks being sold
        symbol = request.form.get("select")
        print(symbol)
        Look = lookup(symbol)
        price = Look["price"]
        shares = request.form.get("shares")

        priceInt = float(price)
        sharesInt = int(shares)

        mult = round((priceInt * sharesInt),2)

        # get session userid
        user = session["user_id"]

        # check users table to ensure user has enough shares of that specific stock to sell
        currentShares = db.execute("SELECT A.purchased - ifnull(A.sold,0) AS shares FROM(\
                                    SELECT t.userId, t.symbol, SUM(t.shares) AS purchased,t1.sold FROM Transactions t\
                                    LEFT JOIN (SELECT t1.userId,t1.symbol, SUM(t1.shares) AS sold FROM Transactions t1\
                                    WHERE t1.userId = :user AND t1.action = 'S' AND t1.symbol = :symbol GROUP BY t1.userId, t1.symbol ) t1 \
                                    ON t1.userId = t.userId AND t1.symbol = t.symbol WHERE t.userId = :user AND t.action = 'P' AND t.symbol = :symbol\
                                    GROUP BY t.userId,t.symbol,t1.sold )A WHERE  A.purchased- ifnull(A.sold,0) > 0",
                                    user=user, symbol=symbol)

        print(currentShares)
        print(type(currentShares))
        currentSharesInt = int(currentShares[0]["shares"])
        print(currentSharesInt)

        currentCash = db.execute("SELECT cash FROM users WHERE id = :user",
                                user=user)

        currentCashInt = int(currentCash[0]["cash"])

        # if the user has at least 1 share of stock
        if currentSharesInt > sharesInt:
            # update users table
            updateUser = db.execute("UPDATE users SET cash = :cash WHERE id = :user",
                                        cash=currentCashInt+mult, user=user)

            # insert record into transaction table
            insert = db.execute("INSERT INTO transactions(userid,symbol,shares,price,action) VALUES(:userid,:symbol,:shares,:price,:action)",
                                                        userid=user, symbol=symbol, shares=sharesInt, price=priceInt, action='S')

        else:
            return apology("Sorry, you do not have enough shares to make this sale")

        # Redirect user to login form
        return redirect("/")

# 7 (personal touch)
@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add money to cash"""
    userId = session["user_id"]
    
    if request.method == "GET":
        return render_template("add.html")
    else:
        # get input
        amount = request.form.get("amount")
        print(amount)
        print(type(amount))
        # query current cash
        currentCash = db.execute("SELECT cash FROM users WHERE id = :userid",
                                userid=userId)
        cc = float(currentCash[0]["cash"])
                                
        newAmount = float(amount) + cc
        
        print(newAmount)
        # update current cash
        updateCash = db.execute("UPDATE users SET cash = :cash WHERE id = :userid",
                                cash=newAmount, userid=userId)
    
    return redirect("/")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)