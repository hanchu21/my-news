import re
from newsapi import NewsApiClient
from flask import flash as f
from dateutil import parser

newsapi = NewsApiClient(api_key='27955b2b10ea4eaf825a2fe98690659e')

class Article(object):
    def __init__(self, source, author, title, description, url, urlToImage, publishedAt, content):
        self.source = source
        self.author = author
        self.title = title
        self.description = description
        self.url = url
        self.urlToImage = urlToImage
        self.publishedAt = parser.parse(publishedAt).strftime("%m/%d/%Y %I:%M:%S %p %Z")
        self.content = content

    @classmethod
    def get_list(cls, category):
        list = []
        articles = newsapi.get_top_headlines(
            category = category,
            language = "en",
            country = "us"
        )["articles"]
        for a in articles:
            list.append(Article(**a))
        return list
    
    @classmethod
    def get_list_by_source(cls, sid):
        list = []
        articles = newsapi.get_everything(
                sources = sid,
                language = "en"
            )["articles"]
        for a in articles:
            list.append(Article(**a))
        return list

    @classmethod
    def search(cls, keyword):
        list = []
        articles = newsapi.get_everything(
                q = keyword,
                language = "en"
            )["articles"]
        for a in articles:
            list.append(Article(**a))
        return list

    @staticmethod
    def validate_search(input):
        is_valid = True
        if len(input["keyword"]) < 2:
            f("Keyword is required and must contain at least 2 characters")
            is_valid = False
        elif re.search("[@_!#$%^&*()<>?/\|}{~:]", input["keyword"]):
            f("Keyword should only contain alphanumeric characters")
            is_valid = False
        return is_valid