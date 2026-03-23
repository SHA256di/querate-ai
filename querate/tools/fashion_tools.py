import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data")
FASHION_PATH = os.path.join(DATA_DIR, "purchases_clean.json")


def _load_data() -> list:
    with open(FASHION_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_purchases() -> dict:
    """Returns all items from the fashion dataset."""
    data = _load_data()
    return {"purchases": data, "count": len(data)}


def get_brands() -> dict:
    """Extracts and returns unique brand and item titles."""
    purchases = _load_data()
    unique_brands = []
    seen = set()

    for item in purchases:
        brand = item.get("brand")
        title = item.get("title")
        if brand and title:
            combo = (brand, title)
            if combo not in seen:
                seen.add(combo)
                unique_brands.append({"brand": brand, "title": title})

    return {"brands": unique_brands, "count": len(unique_brands)}
