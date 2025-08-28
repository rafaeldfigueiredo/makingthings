from datetime import datetime
import os

def sort_entries(entries, sort_key):
    if not sort_key:
        return entries

    match sort_key:
        case "az":
            return sorted(entries, key=lambda e: e.get("text", "").lower())
        case "za":
            return sorted(entries, key=lambda e: e.get("text", "").lower(), reverse=True)
        case "new":
            return sorted(entries, key=lambda e: datetime.strptime(e.get("timestamp", ""), "%Y-%m-%d %H:%M:%S"), reverse=True)
        case "old":
            return sorted(entries, key=lambda e: datetime.strptime(e.get("timestamp", ""), "%Y-%m-%d %H:%M:%S"))
        case _:
            return entries


def filter_entries(entries, search_query=None, tag=None):
    filtered = entries
    if search_query:
        filtered = [entry for entry in filtered if search_query in entry["text"].lower()]
    if tag:
        filtered = [e for e in filtered if tag in e.get("tags", [])]    
    return filtered

def save_image(username,image,entry_id):
    user_folder = os.path.join("static","userImages",username)
    if os.makedirs(user_folder,exists_ok=True):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        ext = os.path.splitext(image.filename)[1] or ".jpeg"
        imagefile = f"{timestamp}_{entry_id}{ext}"