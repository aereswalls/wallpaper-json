import os
import json
from datetime import datetime

CATEGORIES = ["astro", "nature", "colors", "stock", "abstract", "architecture"]
DEFAULT_DATE = datetime.today().strftime("%Y-%m-%d")
BASE_PATH = os.getcwd()

for category in CATEGORIES:
    json_path = os.path.join(BASE_PATH, category, f"{category}.json")
    if not os.path.exists(json_path):
        print(f"[SKIP] {json_path} non trovato.")
        continue

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"[ERRORE] {json_path} non è un JSON valido.")
            continue

    updated = False
    for item in data:
        if "downloadCount" not in item:
            item["downloadCount"] = 0
            updated = True
        if "date" not in item:
            item["date"] = DEFAULT_DATE
            updated = True

    if updated:
        with open(json_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[OK] Aggiornato: {json_path}")
    else:
        print(f"[OK] Già aggiornato: {json_path}")
