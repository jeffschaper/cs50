from flask import Flask, redirect, render_template, request, session
from flask_session import Session

app = Flask(__name__)
# Sessions are not permenant
app.config["SESSION_PERMANENT"] = False
# location of data in filesystem of app
app.config["SESSION_TYPE"] = "filesystem"
# enables sessions for this app
Session(app)

# todos = []

@app.route("/")
def tasks():
    # for the current user, do they already have a key called "todos" inside the current users session dictionary?
    if "todos" not in session:
        # if not, create new key, inside session dictionary called "todos" and set to empty list
        session["todos"] = []
    return render_template("tasks.html", todos=session["todos"])

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        todo = request.form.get("task")
        session["todos"].append(todo)
        return redirect("/")
