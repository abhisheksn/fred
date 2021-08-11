# web_app/routes/home_routes.py

from flask import Blueprint, request, render_template

home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/home")
def index():
    print("HOME...")
    #return "HOME"
    return render_template("home.html")

@home_routes.route("/about")
def about():
    print("ABOUT...")
    #return "ABOUT"
    return render_template("about.html")

@home_routes.route("/form")
def form():
    print("RECOMMENDATION...")
    #return "RECOMMENDATION"
    return render_template("form.html")

@home_routes.route("/contact")
def contact():
    print("CONTACT...")
    #return "FRED FORM"
    return render_template("contact.html")
