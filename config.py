import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change_this_to_a_random_string")
    POSTS_JSON = os.path.join(os.path.dirname(__file__), "data", "posts.json")
    INITIATIVES_JSON = os.path.join(os.path.dirname(__file__), "data", "initiatives.json")
