import os
import json
import re
import boto3
from datetime import datetime

# CONFIGURAZIONE
CATEGORIES = ["astro", "nature", "colors", "stock", "abstract", "architecture", "texture", "dark", "cars"]
ACCOUNT_ID = "7ceb7dc4a392b285add79f4443a8098a"
BUCKET_NAME = "aeres-wallpapers"
REGION = "auto"
ENDPOINT_URL = f"https://{ACCOUNT_ID}.r2.cloudflarestorage.com"
PUBLIC_R2_DOMAIN = "https://pub-9479432483c94d3fa988c0a8c61a8614.r2.dev"

ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")

OUTPUT_DIR = "JSON"

def clean_id(filename):
    name = os.path.splitext(filename)[0]
    return re.sub(r'[^a-zA-Z0-9_-]', '', name.replace(" ", "_"))

# Inizializza boto3 client
s3 = boto3.client(
    "s3",
    region_name=REGION,
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=SECRET_ACCESS_KEY
)

for category in CATEGORIES:
    prefix = f"{category}/"
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
    objects = response.get("Contents", [])
    images = [obj for obj in objects if obj["Key"].lower().endswith((".jpg", ".jpeg", ".png"))]

    old_data = {}
    json_filename = os.path.join(OUTPUT_DIR, f"cloudflare_{category}.json")
    if os.path.exists(json_filename):
        try:
            with open(json_filename, "r") as f:
                for item in json.load(f):
                    old_data[item["id"]] = item
        except Exception:
            print(f"⚠️ Errore lettura {json_filename}, verrà rigenerato.")

    data = []
    for idx, obj in enumerate(images, start=1):
        filename = os.path.basename(obj["Key"])
        file_id = clean_id(filename)
        existing = old_data.get(file_id)

        entry = {
            "id": file_id,
            "title": f"{category.capitalize()} {idx}",
            "url": f"{PUBLIC_R2_DOMAIN}/{obj['Key']}",
            "category": category.capitalize(),
            "date": existing["date"] if existing else datetime.today().strftime("%Y-%m-%d"),
            "downloadCount": existing["downloadCount"] if existing else 0
        }
        data.append(entry)

    with open(json_filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Generato {json_filename} con {len(data)} elementi.")
