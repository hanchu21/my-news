import re
from flask import flash as f
from unicodedata import name
from flask_app.config.mysqlconnection import connect_to_mysql as ctm

db = "my_news_db"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.fname = data["first_name"]
        self.lname = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created = data["created_at"].strftime("%m/%d/%Y %I:%M:%S %p")
        self.updated = data["updated_at"].strftime("%m/%d/%Y %I:%M:%S %p")

    @classmethod
    def add_one_by_reg(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(fname)s, %(lname)s, %(email)s, %(password)s, NOW(), NOW());"
        result = ctm(db).query_db(query, data)
        return result
    
    @classmethod
    def get_one_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = ctm(db).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_one_by_id(cls, uid):
        query = f"SELECT * FROM users WHERE id = {uid}"
        result = ctm(db).query_db(query)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def check_email(email):
        is_valid = True
        query = f"SELECT * FROM users WHERE email = '{email}';"
        result = ctm(db).query_db(query)
        if len(result) > 0:
            f("This email is already registered")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_reg(input):
        is_valid = True
        if len(input["fname"]) < 2:
            f("First name is required and must contain at least 2 characters")
            is_valid = False
        if len(input["lname"]) < 2:
            f("Last name is required and must contain at least 2 characters")
            is_valid = False
        if not EMAIL_REGEX.match(input["email"]):
            f("Email format is invalid")
            is_valid = False
        elif not User.check_email(input["email"]):
            f("Email address is already in use")
            is_valid = False
        if len(input["password"]) < 8:
            f("Password must be at least 8 characters")
            is_valid = False
        elif input["confirm_password"] != input["password"]:
            f("Passwords do not match")
            is_valid = False
        elif (re.search("[0-9]", input["password"]) is None) or (re.search("[A-Z]", input["password"]) is None):
            f("Password must contain 1 uppercase letter, and 1 number")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login(input):
        is_valid = True
        if len(input["login_email"]) < 1:
            f("Email is required")
            is_valid = False
        if len(input["login_password"]) < 1:
            f("Password is required")
            is_valid = False
        return is_valid