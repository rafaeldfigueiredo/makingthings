from datetime import datetime

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