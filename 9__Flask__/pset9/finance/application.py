import os

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


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    orders = db.execute(f"SELECT * FROM orders WHERE user_id = {session['user_id']}")
    cash = db.execute(f"SELECT cash FROM users WHERE id = {session['user_id']}")[0]["cash"]
    rows = {}
    for order in orders:
        if order['transaction_type'] == 0:
            if order['stock'] not in rows:
                data = lookup(order['stock'])
                rows[order['stock']] = {'shares': 1, 'name': data['name'], 'price': data['price'], 'symbol': data['symbol'], 'total': data['price']}
            else:
                rows[order['stock']]['shares'] += 1
                rows[order['stock']]['total'] = rows[order['stock']]['shares'] * rows[order['stock']]['price']
        else:
            rows[order['stock']]['shares'] -= 1
    rows = [row for row in rows.values() if row['shares']]
    total = cash + sum(row['total'] for row in rows)
    return render_template("index.html", rows=rows, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get('shares')
        try:
            shares = int(shares)
        except:
            return apology("must enter a numeric share value")
        if shares < 0:
            return apology("must buy a nonzero number of shares")
        if shares % 1:
            return apology("cannot buy a fractional number of shares")
        info = lookup(symbol)
        if not info:
            return apology("invalid stock ticker")
        cash = db.execute(f"SELECT cash FROM users WHERE id = {session['user_id']}")[0]["cash"]
        price = int(info['price']) * int(shares)
        if cash < price:
            return apology("you don't have enough money to buy this stock")

        cash -= price
        for _ in range(int(shares)):
            db.execute("INSERT INTO orders (user_id, price, stock, transaction_type) VALUES (?, ?, ?, 0)", session["user_id"], info["price"], info["symbol"])
        db.execute(f"UPDATE users SET cash = {cash} WHERE id = {session['user_id']}")

        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    orders = db.execute(f"SELECT * FROM orders WHERE user_id = {session['user_id']} ORDER BY transaction_time DESC")
    return render_template('history.html', rows=orders)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("not symbol provided")
        quote = lookup(symbol)
        if not quote:
            return apology("invalid stock ticker")
        return render_template("quoted.html", quote=quote)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        elif not request.form.get("confirmation"):
            return apology("must confirm password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if rows:
            return apology("that username is already taken")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match")

        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1:
            return apology("unknown register error")
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get('shares')
        info = lookup(symbol)
        if not info:
            return apology("invalid stock ticker")
        price = info['price'] * int(shares)
        cash = db.execute(f"SELECT cash FROM users WHERE id = {session['user_id']}")[0]["cash"]
        cash += price
        for _ in range(shares):
            db.execute("INSERT INTO orders (user_id, price, stock, transaction_type) VALUES (?, ?, ?, 1)", session["user_id"], info["price"], info["symbol"])
        db.execute(f"UPDATE users SET cash = {cash} WHERE id = {session['user_id']}")

        return redirect("/")

    orders = db.execute(f"SELECT * FROM orders WHERE user_id = {session['user_id']}")
    rows = {}
    for order in orders:
        if order['stock'] not in rows:
            rows[order['stock']] = 0
        if not order['transaction_type']:
            rows[order['stock']] += 1
        else:
            rows[order['stock']] -= 1

    return render_template("sell.html", stocks=[key for key, val in rows.items() if val > 0])


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
