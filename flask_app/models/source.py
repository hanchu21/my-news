from flask import flash as f
from unicodedata import name
from flask_app.config.mysqlconnection import connect_to_mysql as ctm
from newsapi import NewsApiClient

db = "my_news_db"
newsapi = NewsApiClient(api_key='27955b2b10ea4eaf825a2fe98690659e')

class Source(object):
    def __init__(self, id, name, description, url, category, language, country):
        self.id = id
        self.name = name
        self.description = description
        self.url = url

    @classmethod
    def add_one(cls, data):
        query = "INSERT INTO sources (user_id, source_id, source_name, created_at, updated_at) VALUES (%(user_id)s, %(source_id)s, %(source_name)s, NOW(), NOW()); "
        result = ctm(db).query_db(query, data)
        return result

    @classmethod
    def get_list(cls):
        list = []
        sources = newsapi.get_sources(language = "en")["sources"]
        for s in sources:
            list.append(Source(**s))
        return list

    @classmethod
    def get_one_by_id(cls, id):
        query = f"SELECT * FROM sources WHERE id = {id}"
        result = ctm(db).query_db(query)
        if len(result) < 1:
            return False
        return result[0]

    @classmethod
    def get_all_by_uid(cls, uid):
        query = f"SELECT * FROM sources WHERE user_id = {uid}"
        results = ctm(db).query_db(query)
        sources = []
        for r in results:
            sources.append(r)
        return sources

    @classmethod
    def delete_one(cls, sid):
        query = f"DELETE FROM sources WHERE id = {sid}"
        result = ctm(db).query_db(query)
        return result

    @staticmethod
    def check_source(sid, uid):
        is_valid = True
        query = f"SELECT source_id FROM sources WHERE user_id = {uid}"
        sources = ctm(db).query_db(query)
        for s in sources:
            if s["source_id"] == sid:
                f("You have already saved this source")
                is_valid = False
        return is_valid