import json
from supabase import create_client

# Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

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
