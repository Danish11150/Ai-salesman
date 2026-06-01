from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from supabase_client import supabase   # ⭐ Supabase import from main.py

website = Blueprint(
    "website",
    __name__,
    template_folder="templates",
    static_folder="static"
)

@website.route("/")
def home():
    return render_template("index.html")


# ⭐ REGISTER (Supabase logic)
@website.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed = generate_password_hash(password)

        supabase.table("user").insert({
            "name": name,
            "email": email,
            "password": hashed
        }).execute()

        return redirect("/login")

    return render_template("register.html")


# ⭐ LOGIN (Supabase logic)
@website.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        result = supabase.table("user").select("*").eq("email", email).execute()

        if result.data:
            user = result.data[0]

            if check_password_hash(user["password"], password):
                session["user_id"] = user["id"]
                return redirect("/dashboard")

        return "Wrong email or password"

    return render_template("login.html")


# ⭐ DASHBOARD (Protected)
@website.route("/dashboard")
def dashboard_page():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("dashboard.html")
