from flask import render_template as rt, request as rq, redirect as rd, session as s, flash as f
from flask_app import app
from flask_app.config import functions as fn
from flask_app.models.source import Source
from flask_app.models.article import Article

@app.route("/sources")
def sources():
    conf_msg = False
    uid = False
    saved_sources = []
    if "save_success" in s:
        s.pop("save_success")
        conf_msg = "Source is successfully saved!"
    if "user_id" in s:
        uid = s["user_id"]
        saved_sources = Source.get_all_by_uid(uid)
    print("Showing all news sources")
    return rt(
        "sources.html",
        nav = "sources",
        title = "My News - News Sources",
        categories = fn.get_categories(),
        is_logged_in = fn.is_logged_in(),
        conf_msg = conf_msg,
        sources = Source.get_list(),
        saved_sources = saved_sources
    )

@app.route("/sources/<sid>")
def source_detail(sid):
    conf_msg = False
    if "save_success" in s:
        s.pop("save_success")
        conf_msg = "Source is successfully saved!"
    is_saved = False
    if fn.is_logged_in():
        saved_sources = Source.get_all_by_uid(s["user_id"])
        for ss in saved_sources:
            if ss["source_id"] == sid:
                is_saved = True
                break
    print(f"Showing articles of source {sid}")
    return rt(
        "source.html",
        nav = "sources",
        title = "My News - Articles from News Source",
        categories = fn.get_categories(),
        is_logged_in = fn.is_logged_in(),
        conf_msg = conf_msg,
        sid = sid,
        articles = Article.get_list_by_source(sid),
        is_saved = is_saved
    )

@app.route("/savesource", methods=["POST"])
def save_source():
    data = {
        "user_id": s["user_id"],
        "source_id": rq.form["source_id"],
        "source_name": rq.form["source_name"],
        "redirect": rq.form["redirect"]
    }
    if not Source.check_source(data["source_id"], data["user_id"]):
        return rd(data["redirect"])
    Source.add_one(data)
    s["save_success"] = True
    print("Source is saved successfully for user")
    return rd(data["redirect"])

@app.route("/deletesource/<sid>")
def delete_source(sid):
    source = Source.get_one_by_id(sid)
    if not source:
        return fn.alert("You do not have this source saved!", "/home")
    if not s["user_id"] or s["user_id"] != source["user_id"]:
        return fn.alert("You do not have permission for this action!", "/home")
    Source.delete_one(sid)
    s["conf_msg"] = "The keyword has been deleted successfully"
    print(f"Keyword {sid} has been deleted")
    return rd("/home")