from flask import Flask, flash, redirect,request,jsonify,render_template,session, url_for
from functools import wraps
import json

app = Flask(__name__)
app.secret_key = "heyitsmegoku"

data_file = "users.json" 

def load_users():
    with open(data_file, "r") as f:
        return json.load(f)

def register_users(userlist):
    with open(data_file, "w") as f:
        return json.dump(userlist,f)
        

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


# === Routes === #
@app.get("/")
def landingPage():
    session_user = session.get("username")
    return render_template('index.html',username=session_user)

@app.get("/api/users")
def get_users_json():
    with open(data_file,"r") as f:
        return jsonify(load_users())

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        if username in [user["name"] for user in load_users()]:
            session["username"] = username
            flash("Success!", category="ok")
            return redirect(url_for("dashboard"))  # make sure this is using url_for
        else:
            flash("Something went wrong!", category="failure")
            return render_template("login.html")
    flash("⚠️ This is a test flash", category="error")
    return render_template("login.html")

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

@app.route("/test-flash")
def test_flash():
    flash("This is a test flash!", category="ok")
    return render_template("login.html")  # must extend base.html


@app.get("/dashboard")
@username_required
def dashboard(username):
    return render_template("dashboard.html", username=username)

@app.get("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)