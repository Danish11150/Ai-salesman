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
    current_category = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.lower().startswith("category:"):
            current_category = {"name": line.split(":")[1].strip(), "items": []}
            data["categories"].append(current_category)

        elif line.lower().startswith("item:"):
            item_name = line.split(":")[1].strip()
            item = {"id": item_name.lower().replace(" ", "_"), "name": item_name}
            current_category["items"].append(item)

        elif line.lower().startswith("price:"):
            price_text = line.split(":")[1].strip().lower()
price_value = ''.join(ch for ch in price_text if ch.isdigit() or ch == '.')
current_category["items"][-1]["price"] = float(price_value) if price_value else 0
current_category["items"][-1]["currency"] = "SAR" if "sar" in price_text else "USD"

        elif line.lower().startswith("stock:"):
            qty = int(line.split(":")[1].strip())
            current_category["items"][-1]["stock_qty"] = qty
            current_category["items"][-1]["in_stock"] = qty > 0

    return data
