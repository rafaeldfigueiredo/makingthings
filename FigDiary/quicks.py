import json, os, shutil

entry_file = "data/entries.json"
static_dir = "static"
new_base = os.path.join(static_dir, "userImages")

with open(entry_file, "r") as f:
    data = json.load(f)

updated = False

for username, entries in data.items():
    for entry in entries:
        image = entry.get("image")
        if image and not image.startswith("userImages/"):
            # Update image path
            entry["image"] = f"userImages/{image}"
            updated = True

            # Move image file if it still exists
            old_path = os.path.join(static_dir, image)
            new_path = os.path.join(static_dir, entry["image"])

            new_dir = os.path.dirname(new_path)
            os.makedirs(new_dir, exist_ok=True)

            if os.path.exists(old_path):
                shutil.move(old_path, new_path)
                print(f"Moved: {old_path} -> {new_path}")
            else:
                print(f"⚠️ File not found: {old_path}")

if updated:
    with open(entry_file, "w") as f:
        json.dump(data, f, indent=2)
    print("✅ entries.json updated successfully.")
else:
    print("ℹ️ No changes needed.")
