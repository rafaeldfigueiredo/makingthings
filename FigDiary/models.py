import json

ENTRY_FILE = "data/entries.json"
USER_FILE = "data/users.json"

def read_json(datafile):
    try:
        with open(datafile, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def write_json(datafile, newdata):
    with open(datafile, "w") as file:
        json.dump(newdata, file)

def load_entries():
    data = read_json(ENTRY_FILE)
    if isinstance(data, dict):
        # Ensure all entries have default keys
        for user_entries in data.values():
            for entry in user_entries:
                entry.setdefault("favorite", False)
                entry.setdefault("private", False)
                entry.setdefault("mood", "")
        return data
    return {}

def save_entries(data):
    write_json(ENTRY_FILE, data)

def load_users():
    return read_json(USER_FILE)

def save_users(data):
    write_json(USER_FILE, data)

def get_user_entries(username):
    all_entries = load_entries()
    return all_entries.get(username, []), all_entries

def get_entry_by_id(username, entry_id):
    user_entries, _ = get_user_entries(username)
    return next((e for e in user_entries if e.get("id") == entry_id), None)

def get_entry_with_parent(username, entry_id):
    user_entries, all_entries = get_user_entries(username)
    entry = next((e for e in user_entries if e.get("id") == entry_id), None)
    return entry, user_entries, all_entries
