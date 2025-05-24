import os
import json
import re
import requests
from datetime import datetime

# CONFIGURAZIONE
CATEGORIES = ["astro", "nature", "colors", "stock", "abstract", "architecture", "texture", "dark", "cars"]
ACCOUNT_ID = "7ceb7dc4a392b285add79f4443a8098a"
BUCKET_NAME = "aeres-wallpapers"
API_TOKEN = "7FX5ZNTjHbGF6uIt3ZiCDwPYCjAlHeLdk-P4rFSF"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def clean_id(filename):
    name = os.path.splitext(filename)[0]
    return re.sub(r'[^a-zA-Z0-9_-]', '', name.replace(" ", "_"))

def list_objects():
    endpoint = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/r2/buckets/{BUCKET_NAME}/objects"
    result = []
    cursor = None

    while True:
        params = {"cursor": cursor} if cursor else {}
        response = requests.get(endpoint, headers=HEADERS, params=params)

        if response.status_code != 200:
            print("❌ Errore nella richiesta:", response.status_code, response.text)
            break

        body = response.json()
        result.extend(body["result"])
        cursor = body.get("result_info", {}).get("cursor")

        if not cursor:
            break

    return result

all_objects = list_objects()

for category in CATEGORIES:
    filtered = [obj for obj in all_objects if obj["key"].startswith(f"{category}/") and obj["key"].lower().endswith((".jpg", ".jpeg", ".png"))]

    old_data = {}
    json_filename = os.path.join("JSON", f"cloudflare_{category}.json")
    if os.path.exists(json_filename):
        try:
            with open(json_filename, "r") as f:
                for item in json.load(f):
                    old_data[item["id"]] = item
        except Exception:
            print(f"⚠️ Errore lettura {json_filename}, verrà rigenerato.")

    data = []
    for idx, obj in enumerate(filtered, start=1):
        filename = os.path.basename(obj["key"])
        file_id = clean_id(filename)
        existing = old_data.get(file_id)

        entry = {
            "id": file_id,
            "title": f"{category.capitalize()} {idx}",
            "url": f"https://{BUCKET_NAME}.r2.cloudflarestorage.com/{obj['key']}",
            "category": category.capitalize(),
            "date": existing["date"] if existing else datetime.today().strftime("%Y-%m-%d"),
            "downloadCount": existing["downloadCount"] if existing else 0
        }
        data.append(entry)

    with open(json_filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Generato {json_filename} con {len(data)} elementi.")
