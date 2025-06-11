import os
import boto3
from urllib.parse import unquote

CATEGORIES = ["astro", "nature", "colors", "stock", "abstract", "architecture", "texture", "dark", "city", "cars"]
ACCOUNT_ID = "7ceb7dc4a392b285add79f4443a8098a"
BUCKET_NAME = "aeres-wallpapers"
REGION = "auto"
ENDPOINT_URL = f"https://{ACCOUNT_ID}.r2.cloudflarestorage.com"

ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")

s3 = boto3.client(
    "s3",
    region_name=REGION,
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=SECRET_ACCESS_KEY
)

for category in CATEGORIES:
    local_dir = os.path.join(".", category)
    os.makedirs(local_dir, exist_ok=True)

    prefix = f"{category}/"
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
    objects = response.get("Contents", [])

    for obj in objects:
        key = obj["Key"]
        if "/thumbs/" in key or not key.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        filename = os.path.basename(unquote(key))
        local_path = os.path.join(local_dir, filename)

        if os.path.exists(local_path):
            continue

        print(f"⬇️  Scarico: {key}")
        s3.download_file(BUCKET_NAME, key, local_path)

print("✅ Download completato.")
