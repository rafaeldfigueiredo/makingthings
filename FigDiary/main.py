from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, flash, redirect,request,render_template,session, url_for
from functools import wraps
import os
import json

app = Flask(__name__)
app.secret_key = "heyitsmegoku"
user_file = "data/users.json" 
entry_file = "data/entries.json"
TIMEFORMAT = "%H:%M:%S"
# ===   === Getter/Setter functions  ===  === #
# Generic JSON files
def read_json(datafile):
    try:
        with open(datafile,"r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
def write_json(datafile,newdata):
    with open(datafile,"w") as file:
        return json.dump(newdata, file)

# Load specific elements
def load_users():
    return read_json(user_file)
def save_users(data):
    write_json(user_file,data)

def load_entries():
    data = read_json(entry_file)
    if isinstance(data,dict):
        for user_entries in data.values():
            for entry in user_entries:
                entry.setdefault("favorite", False)
                entry.setdefault("private", False)
                entry.setdefault("mood", "")
        return data
    return {}
def save_entries(data):
    write_json(entry_file,data)

def get_user_entries(username):
    all_entries = load_entries()
    return all_entries.get(username,[]), all_entries
def get_entry_by_id(username, entry_id):
    user_entries, _ = get_user_entries(username)
    return next((e for e in user_entries if e.get("id") == entry_id), None)
def get_entry_with_parent(username, entry_id):
    '''This is for retrieval of whole list so it can get written in memory'''
    user_entries, all_entries = get_user_entries(username)
    entry = next((e for e in user_entries if e.get("id") == entry_id), None)
    return entry, user_entries, all_entries


# === DecoFunc === #
def username_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        username = session.get("username")
        print("Session username:", username)
        if username not in [user["name"] for user in load_users()]:
            flash("Unauthorized access", category="error")
            return render_template("login.html"), 401
        return func(username=username, *args, **kwargs)
    return wrapper

# ===  ===   === Routes  ===  ===  === #
@app.get("/")
def landingPage():
    session_user = session.get("username")
    return render_template('index.html',username=session_user)

# == Users Logic == #

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        if username in [user["name"] for user in load_users()]:
            session["username"] = username
            flash("Success!", category="ok")
            return redirect(url_for("dashboard"))
        else:
            flash("Something went wrong!", category="error")
            return redirect("/login")
    return render_template("login.html")

@app.get("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        if username == "":
            flash("You can't register with a blank name",category="error")
            return redirect("/register")
        users = load_users()
        entries = load_entries()
        if username not in [user["name"] for user in users]:
            users.append({"name":username})
            save_users(users)

            entries[username] = []
            save_entries(entries)

            session["username"] = username
            flash(message="Registered successfully!", category="ok")
            return redirect(url_for("dashboard"))
        else:
            flash(message="User already exists!", category="error")
            return render_template("register.html")
    return render_template("register.html")

# == CRUD Operations == #

@app.post("/new-entry")
@username_required
def new_entry(username):
    content = request.form.get("new-entry","").strip()
    tags = request.form.get("tags","").strip()
    image = request.files.get("image")
    moods = request.form.get("mood")
    
    if not content:
        flash("You cannot post blank entries!")
        return redirect("/dashboard")
    
    entries = load_entries()
    if username not in entries:
        entries[username] = []
    last_index = len(entries[username]) + 1
    
    new_entry = {
        "id":last_index,
        "text":content,
        "timestamp" : datetime.now().strftime("%H:%M:%S"),
        "favorite":False,
        "mood":moods
    }
    
    if tags:
        new_entry["tags"] = [tag.strip() for tag in tags.split(",")]
    if image and image.filename:
        user_folder = os.path.join("static", "userImages", username)
        os.makedirs(user_folder, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        ext = os.path.splitext(image.filename)[1] or ".jpeg"
        filename = secure_filename(f"{timestamp}_{last_index}{ext}")

        image_path = os.path.join(user_folder, filename)
        image.save(image_path)
        new_entry["image"] = f"userImages/{username}/{filename}"
        
    entries[username].append(new_entry)
    save_entries(entries)
    return redirect("/dashboard")
    
@app.route("/dashboard", methods=["GET", "POST"])
@username_required
def dashboard(username):
    user_entries, _ = get_user_entries(username)
    display_entries = []

    if request.method == "POST":
        query = request.form.get("search", "").lower()
        display_entries = [
            entry for entry in user_entries if query in entry["text"].lower()
        ]
        if not display_entries:
            flash("No results found!")
        return render_template("dashboard.html", username=username, entries=display_entries)

    get_tags = request.args.get("tag")
    get_sorting = request.args.get("sort")

    if get_sorting:
        match get_sorting:
            case "az":
                display_entries = sorted(user_entries, key=lambda e: e["text"].lower())
            case "za":
                display_entries = sorted(user_entries, key=lambda e: e["text"].lower(), reverse=True)
            case "new":
                display_entries = sorted(user_entries, key=lambda e: datetime.strptime(e["timestamp"], "%H:%M:%S"), reverse=True)
            case "old":
                display_entries = sorted(user_entries, key=lambda e: datetime.strptime(e["timestamp"], "%H:%M:%S"))
            case _:
                flash("Something went wrong!")
                return render_template("login.html"), 401
        return render_template("dashboard.html", username=username, entries=display_entries, selected_sort=get_sorting)

    if get_tags:
        display_entries = [e for e in user_entries if get_tags in e.get("tags", [])]
        return render_template("dashboard.html", username=username, entries=display_entries)

    # Default: show all entries
    display_entries = user_entries
    return render_template("dashboard.html", username=username, entries=display_entries)

@app.get("/entry/<int:entry_id>")
@username_required
def entry_detail(username,entry_id):
    user_entries, _ = get_user_entries(username)
    display_entry = next((entry for entry in user_entries if entry.get("id") == entry_id),None)
    if display_entry is None:
        flash("Entry not found", category="error")
        return redirect("/dashboard")
    return render_template("entry-detail.html", entry=display_entry, id=entry_id)

@app.route("/edit_entry/<int:entry_id>", methods=["GET", "POST"])
@username_required
def edit_entry(username, entry_id):
    entry,user_entries,all_entries = get_entry_with_parent(username, entry_id)
    
    if not entry:
        flash("Invalid entry ID", category="error")
        return redirect("/dashboard")


    if request.method == "POST":
        new_content = request.form.get("text", "").strip()
        image = request.files.get("new_image")

        if new_content:
            entry["text"] = new_content

        if image and image.filename:
            user_folder = os.path.join("static", "userImages", username)
            os.makedirs(user_folder, exist_ok=True)

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            ext = os.path.splitext(image.filename)[1] or ".jpeg"
            filename = secure_filename(f"{timestamp}_{entry_id}{ext}")
            new_path = os.path.join(user_folder, filename)

            try:
                image.save(new_path)
                old_image_path = entry.get("image")
                if old_image_path:
                    full_old_path = os.path.join("static", old_image_path)
                    if os.path.exists(full_old_path):
                        os.remove(full_old_path)
                entry["image"] = f"userImages/{username}/{filename}"
            except Exception as e:
                flash("Image upload failed!", category="error")
                print("Error saving image:", e)
                return redirect("/dashboard")

        entry["timestamp"] = datetime.now().strftime("%H:%M:%S")
        save_entries(all_entries)

        flash("Entry updated!", category="ok")
        return redirect("/dashboard")

    return render_template("edit.html", entry=entry, entry_id=entry_id)

@app.post("/toggle-favorite/<int:entry_id>")
@username_required
def favorite_entry(username, entry_id):
    entries, full_list = get_user_entries(username)

    for entry in entries:
        if entry.get("id") == entry_id:
            entry["favorite"] = not entry.get("favorite", False)

    save_entries(full_list)
    return redirect("/dashboard")

@app.post("/toggle-private/<int:entry_id>")
@username_required
def private_entry(username,entry_id):
    entries, full_list = get_user_entries(username)    
    for entry in entries:
        if entry.get("id") == entry_id:
            entry["private"] = not entry.get("private",False)
            break
    save_entries(full_list)
    return redirect("/dashboard")

@app.post("/delete_entry/<int:entry_id>")
@username_required
def delete_entry(username, entry_id):
    entry = get_entry_by_id(username, entry_id)
    if entry is None:
        flash("Entry not found", category="error")
        return redirect("/dashboard")

    entries = load_entries()
    user_entries = entries.get(username, [])

    image_relative_path = entry.get("image")
    if image_relative_path:
        image_full_path = os.path.join("static", image_relative_path)
        if os.path.exists(image_full_path):
            os.remove(image_full_path)

    user_entries.remove(entry)
    save_entries(entries)

    flash("Entry deleted!", category="ok")
    return redirect("/dashboard")

## == Ignition == ##
if __name__ == "__main__":
    app.run(debug=True)