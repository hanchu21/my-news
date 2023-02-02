from flask import session as s

def get_categories(): # This will be updated to a function to grab all categories, either from an API or database
    categories = [
        "general",
        "business",
        "entertainment",
        "health",
        "science",
        "sports",
        "technology"
    ]
    return categories

def alert(msg, path):
    return f"<script>alert('{msg}'); window.location.href = '{path}'</script>"

def is_logged_in():
    if "user_id" in s:
        return True
    return False