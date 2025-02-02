import os
import hashlib
import sqlite3
import random
import math
import hashlib
import ctypes
import tempfile
import secrets

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    make_response,
)
from werkzeug.utils import secure_filename
from base64 import b64decode as sql_secret
from sympy import nextprime


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(32))
JWT_SECRET = "hardcoded-secret-key-123456789"
app.config["SESSION_PERMANENT"] = True

DB_PATH = "db/users.db"
BASE_FILE_DIR = "files"

username_sql = sql_secret(
    "U0VMRUNUIHBhc3N3b3JkIEZST00gdXNlcnMgV0hFUkUgdXNlcm5hbWU9Pw=="
)


def string_to_number(data: str):
    hash_obj = hashlib.sha256(data.encode())
    hash_int = int(hash_obj.hexdigest(), 16)
    return hash_int % (10**9)


def salt(data: str):
    data_number = string_to_number(data.decode())
    SEED = int(math.e * 1e9)
    random.seed(SEED)
    a = nextprime(random.randint(10**8, 10**9))
    b = nextprime(random.randint(10**8, 10**9))
    m = 10**9
    salted_number = (a * data_number + b) % m
    return f"{salted_number:09d}"


def md5_hash(password):
    return hashlib.md5(str(salt(password.encode("utf-8"))).encode("utf-8")).hexdigest()


def auth_exists(user_id):
    db_conn = sqlite3.connect(DB_PATH)
    db_cursor = db_conn.cursor()
    db_cursor.execute(username_sql.decode(), (user_id,))
    user_record = db_cursor.fetchone()
    db_conn.close()
    return (lambda rec: rec[0] if rec else None)(user_record)


def authenticate(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""SELECT password FROM users WHERE username = ?""", (username,))
    result = cursor.fetchone()
    conn.close()

    if auth_exists(username) == md5_hash(password):
        return True
    return False


def get_files(path):
    full_path = os.path.join(BASE_FILE_DIR, path)
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    entries = []
    for entry in os.listdir(full_path):
        entry_path = os.path.join(full_path, entry)
        entries.append({"name": entry, "is_dir": os.path.isdir(entry_path)})

    return entries, full_path


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    account_exists = auth_exists(username)

    if (account_exists != None) and (authenticate(username, password)):
        session["username"] = username
        response = make_response(redirect(url_for("files")))
    elif account_exists:
        flash("Invalid credentials, please check your password")
        response = make_response(redirect(url_for("index")))
        response.set_cookie(
            "sessid", account_exists, max_age=3600, httponly=True, secure=True
        )
    else:
        flash("Username does not exist")
        response = make_response(redirect(url_for("index")))

    return response


@app.route("/files/", defaults={"subpath": ""})
@app.route("/files/<path:subpath>")
def files(subpath):
    if "username" not in session:
        return redirect(url_for("index"))

    current_path = os.path.join(BASE_FILE_DIR, session["username"], subpath)
    if not os.path.exists(current_path):
        return "Not Found", 404

    if request.args.get("file"):
        selected_file = secure_filename(request.args["file"])
        file_path = os.path.join(current_path, selected_file)
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                file_contents = f.read()
            return render_template(
                "file_viewer.html", file_contents=file_contents, subpath=subpath
            )
        else:
            return "Not Found", 404

    file_list, full_path = get_files(os.path.join(session["username"], subpath))
    return render_template("file_explorer.html", file_list=file_list, subpath=subpath)


@app.route("/create", methods=["POST"])
def create():
    if "username" not in session:
        return redirect(url_for("index"))

    item_type = request.form["type"]
    name = request.form["name"]
    subpath = request.form["subpath"]

    current_path = os.path.join(BASE_FILE_DIR, session["username"], subpath)

    if item_type == "folder":
        os.makedirs(os.path.join(current_path, name), exist_ok=True)
    elif item_type == "file":
        with open(os.path.join(current_path, name), "w") as f:
            f.write("")

    return redirect(url_for("files", subpath=subpath))


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route("/about")
def about():
    return render_template("aboutus.html")


@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy.html")


@app.route("/animal-testing-statement")
def animal_testing():
    return render_template("animal_testing.html")


if __name__ == "__main__":
    app.run(debug=False)
