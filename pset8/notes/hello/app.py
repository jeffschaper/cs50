import random
from flask import Flask, render_template, request
# variable to represent flask application
# __name__ = service application from this file
app = Flask(__name__)

# Routes - Different pages to access.  Example google.com/images
# default route /
@app.route("/")
# each route is associated with a function that runs when visited
def index():
    number = random.randint(0,1)
    return render_template("index.html", number=number)

@app.route("/goodbye")
def bye():
    return "Goodbye!"

@app.route("/hello")
def hello():
    name = request.args.get("name")
    if not name: 
        return render_template("failure.html")
    return render_template("hello.html", name=name)