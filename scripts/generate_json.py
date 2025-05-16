import os
import json

CATEGORIES = ["nature", "abstract", "astro", "city", "minimal"]
BASE_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/wallpaper-json/main/"

for category in CATEGORIES:
    files = os.listdir(category)
    images = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    data = []
    for idx, filename in enumerate(images, start=1):
        entry = {
            "id": f"{category}{idx}",
            "title": f"{category.capitalize()} {idx}",
            "url": f"{BASE_URL}{category}/{filename}",
            "category": category.capitalize(),
            "downloads": 0
        }
        data.append(entry)

    with open(f"{category}/{category}.json", "w") as f:
        json.dump(data, f, indent=2)
