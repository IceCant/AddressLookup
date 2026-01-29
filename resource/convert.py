import csv
import json
from collections import defaultdict

# Input CSV file
csv_file = "data.csv"

# Output JSON file
json_file = "data.json"

# Nested dictionary: province -> district -> commune -> village
locations = defaultdict(lambda: defaultdict(dict))

with open(csv_file, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        p_code = row['province_code']   # keep as string to preserve leading zeros
        d_code = row['district_code']
        c_code = row['commune_code']
        v_code = row['village_code']

        # Initialize province if not exists
        if p_code not in locations:
            locations[p_code] = {
                "name_kh": row["province_kh"],
                "name_en": row["province_en"],
                "districts": {}
            }

        # Initialize district if not exists
        if d_code not in locations[p_code]["districts"]:
            locations[p_code]["districts"][d_code] = {
                "name_kh": row["district_kh"],
                "name_en": row["district_en"],
                "communes": {}
            }

        # Initialize commune if not exists
        if c_code not in locations[p_code]["districts"][d_code]["communes"]:
            locations[p_code]["districts"][d_code]["communes"][c_code] = {
                "name_kh": row["commune_kh"],
                "name_en": row["commune_en"],
                "villages": {}
            }

        # Add village
        locations[p_code]["districts"][d_code]["communes"][c_code]["villages"][v_code] = {
            "name_kh": row["village_kh"],
            "name_en": row["village_en"]
        }

# Convert defaultdict to normal dict
locations_dict = json.loads(json.dumps(locations))

# Save to JSON file
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(locations_dict, f, ensure_ascii=False, indent=2)

print(f"Saved nested JSON to {json_file}")
