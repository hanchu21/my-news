from flask import render_template as rt, request as rq, redirect as rd, session as s, flash as f
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.config import functions as fn
from flask_app.models.user import User
from flask_app.models.keyword import Keyword
from flask_app.models.source import Source

bcrypt = Bcrypt(app)

@app.route("/signin")
def signin():
    if fn.is_logged_in():
        return rd("/home")
    reg_input = False
    login_input = False
    if "reg_input" in s:
        reg_input = s["reg_input"]
        s.pop("reg_input")
    if "login_input" in s:
        login_input = s["login_input"]
        s.pop("login_input")
    print("Displaying registration and login forms")
    return rt(
        "signin.html", 
        title = "My News - Sign Up or Log In", 
        reg_input = reg_input, 
        login_input = login_input,
        is_logged_in = fn.is_logged_in(),
        categories = fn.get_categories()
    )

@app.route("/register", methods=["POST"])
def register():
    if not User.validate_reg(rq.form):
        s["reg_input"] = rq.form
        return rd("/signin")
    pw_hash = bcrypt.generate_password_hash(rq.form["password"])
    data = {
        "fname": rq.form["fname"],
        "lname": rq.form["lname"],
        "email": rq.form["email"],
        "password": pw_hash
    }
    id = User.add_one_by_reg(data)
    s['user_id'] = id
    print(f"User {id} is registered and logged in")
    return rd("/home")

@app.route("/login", methods=["POST"])
def login():
    if not User.validate_login(rq.form):
        s["login_input"] = rq.form
        return rd("/signin")
    data = { "email": rq.form["login_email"] }
    user = User.get_one_by_email(data)
    if not user or not bcrypt.check_password_hash(user.password, rq.form["login_password"]):
        s["login_input"] = rq.form
        f("Invalid Email/Password")
        return rd("/signin")
    s['user_id'] = user.id
    print(f"User {user.id} is now logged in")
    return rd("/home")

@app.route("/home")
def home():
    conf_msg = False
    if not fn.is_logged_in():
        return fn.alert("Please log in first", "/")
    uid = s["user_id"]
    if "conf_msg" in s:
        conf_msg = s["conf_msg"]
        s.pop("conf_msg")
    print(f"Showing account home for user {uid}")
    return rt(
        "home.html", 
        title = "My News - Account Home",
        categories = fn.get_categories(),
        conf_msg = conf_msg,
        is_logged_in = fn.is_logged_in(),
        u = User.get_one_by_id(uid),
        keywords = Keyword.get_all_by_uid(uid),
        sources = Source.get_all_by_uid(uid)
    )

@app.route("/logout")
def logout():
    s.clear()
    print("User is now logged out")
    return rd("/")