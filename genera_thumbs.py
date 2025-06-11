import os
from PIL import Image

CATEGORIES = ["astro", "nature", "colors", "stock", "abstract", "architecture", "texture", "dark", "city", "cars"]
THUMB_SIZE = (720, 1280)

def crea_thumbnail(input_path, output_path):
    with Image.open(input_path) as img:
        img.thumbnail(THUMB_SIZE)

if img.mode in ("RGBA", "P"):
    img = img.convert("RGB")

img.save(output_path, format="JPEG", quality=85)


for category in CATEGORIES:
    input_dir = os.path.join(".", category)
    thumbs_dir = os.path.join(input_dir, "thumbs")
    os.makedirs(thumbs_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            input_path = os.path.join(input_dir, file)
            output_path = os.path.join(thumbs_dir, file)
            if not os.path.exists(output_path):
                crea_thumbnail(input_path, output_path)
                print(f"✅ Creato: {output_path}")
