import os
import json
import re
from datetime import datetime

CATEGORIES = ["astro", "nature", "colors", "stock", "abstract", "architecture", "texture", "dark", "cars"]
BASE_URL = "https://raw.githubusercontent.com/aereswalls/wallpaper-json/main/"

def clean_id(filename):
    name = os.path.splitext(filename)[0]
    return re.sub(r'[^a-zA-Z0-9_-]', '', name.replace(" ", "_"))

for category in CATEGORIES:
    path = os.path.join(os.getcwd(), category)
    if not os.path.exists(path):
        print(f"Cartella non trovata: {path}")
        continue

    files = os.listdir(path)
    images = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png", ".JPG", ".PNG"))]

    # Carica JSON esistente (se disponibile)
    json_path = os.path.join(path, f"{category}.json")
    old_data = {}
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            try:
                for item in json.load(f):
                    old_data[item["id"]] = item
            except Exception:
                print(f"⚠️ Errore lettura {json_path}, verrà rigenerato.")
                old_data = {}

    data = []
    for idx, filename in enumerate(images, start=1):
        file_id = clean_id(filename)
        existing = old_data.get(file_id)

        entry = {
            "id": file_id,
            "title": f"{category.capitalize()} {idx}",
            "url": f"{BASE_URL}{category}/{filename}",
            "category": category.capitalize(),
            "date": existing["date"] if existing else datetime.today().strftime("%Y-%m-%d"),
            "downloadCount": existing["downloadCount"] if existing else 0
        }
        data.append(entry)

    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Generato {category}.json con {len(data)} elementi.")
