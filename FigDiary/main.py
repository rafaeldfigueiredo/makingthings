from datetime import datetime
from werkzeug.utils import secure_filename
import os
from flask import Flask, flash, redirect,request,jsonify,render_template,session, url_for
from functools import wraps
import json

app = Flask(__name__)
app.secret_key = "heyitsmegoku"

data_file = "data/users.json" 
entry_file = "data/entries.json"
# ===   === Getter/Setter functions  ===  === #
def load_users():
    with open(data_file, "r") as f:
        return json.load(f)

def register_users(userlist):
    with open(data_file, "w") as f:
        return json.dump(userlist,f)

def load_entries():
    try:
        with open(entry_file, "r") as f:
            data = json.load(f)
            if isinstance(data,dict):
                return data
            else:
                return {}
    except FileNotFoundError:
        return {}
        
def register_entries(entrylist):
    with open(entry_file, "w") as f:
        return json.dump(entrylist,f)

# === DecoFunc for auth === #
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
            return render_template("login.html")
    return render_template("login.html")

@app.get("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        if username not in [user["name"] for user in load_users()]:
            userlist = load_users()
            userlist.append({"name": username})
            register_users(userlist)
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
        "favorite":False
    }
    
    if tags:
        new_entry["tags"] = [tag.strip() for tag in tags.split(",")]
    if image and image.filename:
        user_folder = os.path.join("static", username)
        os.makedirs(user_folder,exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        ext = os.path.splitext(image.filename)[1] or ".jpeg"
        filename =  secure_filename(f"{timestamp}_{last_index}{ext}")
        
        image_path = os.path.join(user_folder,filename)
        image.save(image_path)
        
        new_entry["image"] = f"{username}/{filename}"
        
    entries[username].append(new_entry)
    register_entries(entries)
    return redirect("/dashboard")
    

@app.route("/dashboard", methods=["GET","POST"])
@username_required
def dashboard(username):
    entries = load_entries()
    display_entries = []
    if request.method == "POST":
        query = request.form.get("search")        
        for entry in entries[username]:
            if query.lower() in entry["text"].lower():
                display_entries.append(entry)
                print(display_entries)
            flash("No results found!")
            return redirect("/dashboard")
        return render_template("dashboard.html",username=username, entries=display_entries)
    elif request.method == "GET":
        get_tags = request.args.get("tag")
        get_sorting = request.args.get("sort")
        user_entries = entries.get(username, [])
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
            return render_template("dashboard.html", username=username, entries=display_entries,selected_sort=get_sorting)

        if get_tags:
            for entry in entries[username]:
                if get_tags in entry.get("tags",[]):
                    display_entries.append(entry)
            return render_template("dashboard.html",username=username, entries=display_entries)
        if username not in entries:
            entries[username] = []
            register_entries(entries)
        for entry in entries[username]:
            display_entries.append(entry)
        return render_template("dashboard.html", username=username, entries=display_entries)

@app.post("/toggle-favorite/<int:entry_id>")
@username_required
def favorite_entry(username,entry_id):
    entry_id = entry_id
    full_list = load_entries()
    user_data = full_list.get(username,[])
    for entry in user_data:
        if entry["id"] == entry_id:
            entry["favorite"] = not entry.get("favorite",False)
            break
    register_entries(full_list)
    return redirect("/dashboard")

@app.get("/entry/<int:entry_id>")
@username_required
def entry_detail(entry_id,username):
    entries = load_entries()
    display_entry = entries[username][entry_id]
    return render_template("entry-detail.html",entry=display_entry,id=entry_id)

@app.route("/edit-entry/<int:entry_id>", methods=["GET", "POST"])
@username_required
def edit_entry(entry_id, username):
    full_list = load_entries()
    entry_to_edit = full_list.get(username, [])

    if request.method == "POST":
        new_content = request.form.get("text", "").strip()
        if 0 <= entry_id < len(entry_to_edit):
            entry_to_edit[entry_id]["text"] = new_content
            entry_to_edit[entry_id]["timestamp"] = datetime.now().strftime("%H:%M:%S")
            register_entries(full_list)
            flash("Edit successful!", category="ok")
            return redirect("/dashboard")
    elif request.method == "GET":
        entry = entry_to_edit[entry_id]
        return render_template("edit.html", entry=entry, entry_id=entry_id)
    flash("Something went wrong!",category="error")
    return redirect("/dashboard")
        
@app.post("/delete-entry")
@username_required
def delete_entry(username):
    entry_index = int(request.form.get("entry-id"))
    if username:
        try:
            entries = load_entries()
            for entry in entries[username]:
                image_path = entry.get("image")
                if image_path:
                    full_path = os.path.join("static",image_path)
                    if os.path.exists(full_path):
                        os.remove(full_path)
            entries[username].pop(entry_index)
            register_entries(entries)
            flash("Deleted!",category="ok")
            return redirect("/dashboard")
        except IndexError:
            flash("Invalid entry index", category="error")
            return redirect("/dashboard")
    else:
        flash("You need to login",category="error")
        return redirect("/login")

## == Ignition == ##
if __name__ == "__main__":
    app.run(debug=True)