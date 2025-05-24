import os
import json
import glob

output_file = "cloudflare_master.json"
json_files = glob.glob("cloudflare_*.json")

all_data = []

for file_path in json_files:
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            all_data.extend(data)
    except Exception as e:
        print(f"❌ Errore nella lettura di {file_path}: {e}")

# Scrivi il file master
with open(output_file, "w") as f:
    json.dump(all_data, f, indent=2)

print(f"✅ Generato {output_file} con {len(all_data)} elementi totali.")
