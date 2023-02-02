import re
from flask import flash as f
from unicodedata import name
from flask_app.config.mysqlconnection import connect_to_mysql as ctm

db = "my_news_db"

class Keyword:
    def __init__(self, data):
        self.id = data["id"]
        self.keyword = data["keyword"]
        self.uid = data["user_id"]

    @classmethod
    def add_one(cls, data):
        query = "INSERT INTO keywords (user_id, keyword, created_at, updated_at) VALUES (%(user_id)s, %(keyword)s, NOW(), NOW()); "
        result = ctm(db).query_db(query, data)
        return result

    @classmethod
    def get_all_by_uid(cls, uid):
        query = f"SELECT * FROM keywords WHERE user_id = {uid}"
        results = ctm(db).query_db(query)
        keywords = []
        for r in results:
            keywords.append(cls(r))
        return keywords

    @classmethod
    def get_one_by_id(cls, id):
        query = f"SELECT * FROM keywords WHERE id = {id}"
        result = ctm(db).query_db(query)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def update_one(cls, kid, data):
        query = f"UPDATE keywords SET keyword = %(keyword)s WHERE id = {kid};"
        result = ctm(db).query_db(query, data)
        return result

    @classmethod
    def delete_one(cls, kid):
        query = f"DELETE FROM keywords WHERE id = {kid}"
        result = ctm(db).query_db(query)
        return result

    @staticmethod
    def check_keyword(keyword, uid):
        is_valid = True
        if len(keyword) < 2:
            f("Keyword is required and must contain at least 2 characters")
            is_valid = False
        elif re.search("[@_!#$%^&*()<>?/\|}{~:]", keyword):
            f("Keyword should only contain alphanumeric characters")
            is_valid = False
        query = f"SELECT keyword FROM keywords WHERE user_id = {uid}"
        keywords = ctm(db).query_db(query)
        for k in keywords:
            if k["keyword"] == keyword:
                f("You have already saved this keyword")
                is_valid = False
        return is_valid
