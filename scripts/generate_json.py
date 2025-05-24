import os
import json
import re
from datetime import datetime
from colorthief import ColorThief
import webcolors

CATEGORIES = ["astro", "nature", "colors", "stock", "abstract", "architecture", "texture", "dark"]
BASE_URL = "https://raw.githubusercontent.com/aereswalls/wallpaper-json/main/"

def clean_id(filename):
    name = os.path.splitext(filename)[0]
    return re.sub(r'[^a-zA-Z0-9_-]', '', name.replace(" ", "_"))

def closest_color(requested_color):
    min_colors = {}
    for key, name in webcolors.CSS3_NAMES_TO_HEX.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(name)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = key
    return min_colors[min(min_colors)]

for category in CATEGORIES:
    path = os.path.join(os.getcwd(), category)
    if not os.path.exists(path):
        print(f"Cartella non trovata: {path}")
        continue

    files = os.listdir(path)
    images = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png", ".JPG", ".PNG"))]

    data = []
    for idx, filename in enumerate(images, start=1):
        file_path = os.path.join(path, filename)
        print(f"▶️ Elaborando immagine: {filename}")
        try:
            color_thief = ColorThief(file_path)
            dominant_rgb = color_thief.get_color(quality=1)
            dominant_name = closest_color(dominant_rgb)
            print(f"   → Colore dominante: {dominant_name} ({dominant_rgb})")
        except Exception as e:
            print(f"⚠️ Errore con {filename}: {e}")
            dominant_name = "unknown"

        file_id = clean_id(filename)
        entry = {
            "id": file_id,
            "title": f"{category.capitalize()} {idx}",
            "url": f"{BASE_URL}{category}/{filename}",
            "category": category.capitalize(),
            "date": datetime.today().strftime("%Y-%m-%d"),
            "downloadCount": 0,
            "dominantColor": dominant_name
        }
        data.append(entry)

    json_path = os.path.join(path, f"{category}.json")
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ File JSON generato: {json_path} ({len(data)} elementi)\n")

