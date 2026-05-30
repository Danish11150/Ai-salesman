from flask import Blueprint, render_template

website = Blueprint(
    "website",
    __name__,
    template_folder="templates",
    static_folder="static"
)

@website.route("/")
def home():
    return render_template("index.html")

@website.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")
    
    @website.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")
    @website.route("/dashboard")
def dashboard_page():
      return render_template("dashboard.html")
