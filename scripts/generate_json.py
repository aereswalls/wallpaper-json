import os
import json

CATEGORIES = ["astro", "nature", "colors", "stock", "abstract", "architecture"]
BASE_URL = "https://raw.githubusercontent.com/aereswalls/wallpaper-json/main/"

for category in CATEGORIES:
    path = os.path.join(os.getcwd(), category)
    if not os.path.exists(path):
        continue

    files = os.listdir(path)
    images = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    data = []
    for idx, filename in enumerate(images, start=1):
        file_id = os.path.splitext(filename)[0]  # Use filename (without extension) as ID
        entry = {
            "id": file_id,
            "title": f"{category.capitalize()} {idx}",
            "url": f"{BASE_URL}{category}/{filename}",
            "category": category.capitalize(),
            "downloads": 0
        }
        data.append(entry)

    with open(os.path.join(path, f"{category}.json"), "w") as f:
        json.dump(data, f, indent=2)
