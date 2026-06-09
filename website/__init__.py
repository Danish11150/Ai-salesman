from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from supabase_client import supabase   # ⭐ Supabase import from main.py
from website.inventory import load_inventory
import json
from flask import request, redirect, render_template, session


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

@website.route("/upload_inventory", methods=["GET", "POST"])
def upload_inventory():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        file = request.files["file"]

        # Detect file type
        if file.filename.endswith(".txt"):
            from website.inventory import txt_to_json
            data = txt_to_json(file)
        else:
            data = json.load(file)

        # Send to inventory engine
        load_inventory(data)

        return redirect("/inventory")

    return render_template("upload_inventory.html")


@website.route("/inventory")
def inventory_page():
    if "user_id" not in session:
        return redirect("/login")

    # Get shop_id from URL
    shop_id = request.args.get("shop_id")

    if not shop_id:
        return "Error: shop_id is missing"
        
    # Import inside function (best practice)
    from website.inventory import get_inventory

    # Fetch all items from database
    items = get_inventory()

    # Send items to HTML page
    return render_template("inventory.html", items=items)

@website.route("/create_inventory", methods=["POST"])
def create_inventory():
    if "user_id" not in session:
        return redirect("/login")

    category = request.form["category"]
    name = request.form["name"]
    price = float(request.form["price"])
    stock_qty = int(request.form["stock_qty"])

    item = {
        "id": name.lower().replace(" ", "_"),
        "name": name,
        "price": price,
        "stock_qty": stock_qty,
        "in_stock": stock_qty > 0
    }

    from website.inventory import save_item
    save_item("manual", category, item)

    return redirect("/inventory")




@website.route("/delete_item/<item_id>")
def delete_item(item_id):
    supabase.table("inventory").delete().eq("id", item_id).execute()
    return redirect("/inventory")

@website.route("/edit_item/<item_id>")
def edit_item(item_id):
    item = supabase.table("inventory").select("*").eq("id", item_id).execute().data
    if not item:
        return "Item not found"
    return render_template("edit_item.html", item=item[0])


@website.route("/update_item/<item_id>", methods=["POST"])
def update_item(item_id):
    name = request.form["name"]
    price = float(request.form["price"])
    stock_qty = int(request.form["stock_qty"])

    supabase.table("inventory").update({
        "name": name,
        "price": price,
        "stock_qty": stock_qty,
        "in_stock": stock_qty > 0
    }).eq("id", item_id).execute()

    return redirect("/inventory")

@website.route("/create_shop", methods=["GET", "POST"])
def create_shop():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        name = request.form["name"]
        industry = request.form["industry"]

        supabase.table("shops").insert({
            "user_id": session["user_id"],
            "name": name,
            "industry": industry,
            "plan": "basic"
        }).execute()

        return redirect("/my_shops")

    return render_template("create_shop.html")

@website.route("/my_shops")
def my_shops():
    if "user_id" not in session:
        return redirect("/login")

    shops = supabase.table("shops").select("*").eq("user_id", session["user_id"]).execute().data
    return render_template("my_shops.html", shops=shops)
