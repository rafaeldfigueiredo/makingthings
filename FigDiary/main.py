from datetime import datetime
from flask import Flask, flash, redirect,request,jsonify,render_template,session, url_for
from functools import wraps
import json

app = Flask(__name__)
app.secret_key = "heyitsmegoku"

data_file = "data/users.json" 
entry_file = "data/entries.json"

# == Getter and Setter functions == #
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
            return render_template("error.html"), 401
        return func(username=username, *args, **kwargs)
    return wrapper

# ===  === Routes ===  === #
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
    content = request.form.get("new-entry","")
    tags = request.form.get("tags","")
    if content:
        if username:
            entries = load_entries()
            if username not in entries:
                entries[username] = []
            last_index = len(entries[username]) + 1
            if tags:
                entries[username].append({"id":last_index,"text":content.strip(),"timestamp":datetime.now().strftime("%H:%M:%S"),"tags":tags.split(',')})
            else:
                entries[username].append({"id":last_index,"text":content.strip(),"timestamp":datetime.now().strftime("%H:%M:%S")})
            register_entries(entries)
            return redirect("/dashboard")
        else:
            flash("You need to login",category="error")
            return redirect("/login")
    flash("You cannot post blank entries!")
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