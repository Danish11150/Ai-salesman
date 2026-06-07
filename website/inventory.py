import json
from supabase_client import supabase   # <-- Correct import

def load_inventory(json_data):
    industry = json_data["industry"]

    for category in json_data["categories"]:
        category_name = category["name"]

        for item in category["items"]:
            save_item(industry, category_name, item)


def save_item(industry, category, item):
    supabase.table("inventory").insert({
        "industry": industry,
        "category": category,
        "item_id": item["id"],
        "name": item["name"],
        "description": item.get("description", ""),
        "price": item.get("price", 0),
        "currency": item.get("currency", "SAR"),
        "in_stock": item.get("in_stock", True),
        "stock_qty": item.get("stock_qty", 0),
        "tags": item.get("tags", []),
        "meta": item.get("meta", {})
    }).execute()

def get_inventory():
    result = supabase.table("inventory").select("*").execute()
    return result.data


def txt_to_json(file):
    lines = file.read().decode("utf-8").splitlines()
    data = {"industry": "manual", "categories": []}

    # Auto category (because user never writes category)
    current_category = {"name": "General", "items": []}
    data["categories"].append(current_category)

    last_item = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Detect ITEM (supports: "1. Item: Laptop", "Item: Laptop", "Laptop")
        if "item:" in line.lower():
            item_name = line.split("item:", 1)[1].strip()
        elif line[0].isdigit() and "item" in line.lower():
            item_name = line.split("item", 1)[1].replace(":", "").strip()
        elif line.lower().startswith("item"):
            item_name = line.split(":", 1)[1].strip()
        else:
            item_name = None

        if item_name:
            last_item = {
                "id": item_name.lower().replace(" ", "_"),
                "name": item_name,
                "price": 0,
                "stock_qty": 0,
                "in_stock": True,
                "currency": "SAR"
            }
            current_category["items"].append(last_item)
            continue

        # Detect QUANTITY (supports: "Quantity: 5", "Qty: 5", "QTY 5")
        if "quantity" in line.lower() or "qty" in line.lower():
            if last_item:
                qty = ''.join(ch for ch in line if ch.isdigit())
                last_item["stock_qty"] = int(qty) if qty else 0
                last_item["in_stock"] = last_item["stock_qty"] > 0
            continue

        # Detect PRICE (supports: "Price: 1200 sar", "1200", "1200 SAR")
        if "price" in line.lower():
            if last_item:
                price_text = line.split(":", 1)[1].strip().lower()
                price_value = ''.join(ch for ch in price_text if ch.isdigit() or ch == '.')
                last_item["price"] = float(price_value) if price_value else 0
                last_item["currency"] = "SAR" if "sar" in price_text else "USD"
            continue

    return data
