from flask import render_template as rt, request as rq, redirect as rd, session as s, flash as f
from flask_app import app
from flask_app.config import functions as fn
from flask_app.models.article import Article
from flask_app.models.keyword import Keyword

@app.route("/")
def default():
    print(f"Showing the default list view of articles")
    return rd("/news/general")

@app.route("/news/<category>")
def list(category):
    if category not in fn.get_categories():
        return fn.alert("This category does not exist!", "/")
    print(f"Showing the category list view of articles")
    return rt(
        "index.html",
        title = "My News - " + category.capitalize() + " Headlines",
        nav = "category",
        categories = fn.get_categories(),
        category = category,
        is_logged_in = fn.is_logged_in(),
        articles = Article.get_list(category)
    )

@app.route("/search")
def search():
    print(f"Showing the search form")
    return rt(
        "search.html",
        nav = "search",
        title = "My News - Search",
        categories = fn.get_categories(),
        is_logged_in = fn.is_logged_in()
    )

@app.route("/searchbykeyword", methods = ["POST"])
def search_by_keyword():
    if "keyword" not in rq.form or not Article.validate_search(rq.form):
        return rd("/search")
    s["recent_keyword"] = rq.form["keyword"]
    print(f"Performing search on the keyword `{rq.form['keyword']}`")
    return rd("/results")

@app.route("/results")
def search_result():
    keyword = s["recent_keyword"]
    conf_msg = False
    if "save_success" in s:
        s.pop("save_success")
        conf_msg = "Keyword is successfully saved!"
    is_saved = False
    if fn.is_logged_in():
        saved_keywords = Keyword.get_all_by_uid(s["user_id"])
        for sk in saved_keywords:
            if sk.__dict__["keyword"] == keyword:
                is_saved = True
                break
    print(f"Showing search results on the keyword `{keyword}`")
    return rt(
        "results.html",
        title = "My News - Search Results",
        nav = "search",
        categories = fn.get_categories(),
        keyword = keyword,
        is_logged_in = fn.is_logged_in(),
        conf_msg = conf_msg,
        articles = Article.search(keyword),
        is_saved = is_saved
    )