from flask import render_template as rt, request as rq, redirect as rd, session as s, flash as f
from flask_app import app
from flask_app.config import functions as fn
from flask_app.models.keyword import Keyword

@app.route("/savekeyword", methods = ["POST"])
def save_keyword():
    data = {
        "user_id": s["user_id"],
        "keyword": rq.form["save_keyword"]
    }
    if not Keyword.check_keyword(data["keyword"], data["user_id"]):
        return rd("/results")
    Keyword.add_one(data)
    s["save_success"] = True
    print("Keyword is saved successfully for user")
    return rd("/results")    

@app.route("/updatekeyword/", methods = ["POST"])
def update_keyword():
    data = {
        "id": rq.form["id"],
        "keyword": rq.form["save_keyword"],
        "user_id": s["user_id"]
    }
    kid = data["id"]
    keyword = Keyword.get_one_by_id(kid)
    if not keyword:
        return fn.alert("This keyword does not exist!", "/home")
    if not s["user_id"] or s["user_id"] != keyword["user_id"]:
        return fn.alert("You do not have permission for this action!", "/home")
    if not Keyword.check_keyword(data["keyword"], data["user_id"]):
        return rd("/home")
    Keyword.update_one(kid, data)
    s["conf_msg"] = "The keyword has been updated successfully"
    print(f"Keyword {kid} has been updated")
    return rd("/home")

@app.route("/deletekeyword/<kid>")
def delete_keyword(kid):
    keyword = Keyword.get_one_by_id(kid)
    if not keyword:
        return fn.alert("This keyword does not exist!", "/home")
    if not s["user_id"] or s["user_id"] != keyword["user_id"]:
        return fn.alert("You do not have permission for this action!", "/home")
    Keyword.delete_one(kid)
    s["conf_msg"] = "The keyword has been deleted successfully"
    print(f"Keyword {kid} has been deleted")
    return rd("/home")