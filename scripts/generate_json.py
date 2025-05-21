import os
import json
import re
from datetime import datetime

CATEGORIES = ["astro", "nature", "colors", "stock", "abstract", "architecture"]
BASE_URL = "https://raw.githubusercontent.com/aereswalls/wallpaper-json/main/"

def clean_id(filename):
    name = os.path.splitext(filename)[0]
    return re.sub(r'[^a-zA-Z0-9_-]', '', name.replace(" ", "_"))

for category in CATEGORIES:
    path = os.path.join(os.getcwd(), category)
    if not os.path.exists(path):
        continue

    files = os.listdir(path)
    images = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    data = []
    for idx, filename in enumerate(images, start=1):
        file_id = clean_id(filename)
        entry = {
            "id": file_id,
            "title": f"{category.capitalize()} {idx}",
            "url": f"{BASE_URL}{category}/{filename}",
            "category": category.capitalize(),
            "date": datetime.today().strftime("%Y-%m-%d"),
            "downloadCount": 0
        }
        data.append(entry)

    with open(os.path.join(path, f"{category}.json"), "w") as f:
        json.dump(data, f, indent=2)
