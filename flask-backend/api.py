from flask import Flask, escape
from dotenv import load_dotenv

app = Flask(__name__)

"""
landing page:
"""
@app.route("/")
def index():
    return "<p>hello, world!</p>"

"""
user profile page:
"""
@app.route("/u/<user_id>")
def user_profile(user_id):
    return f"{escape(user_id)}'s profile"

"""
injection demo route:
"""
@app.route("/i/<unescaped>")
def injection(unescaped):
    return f"{unescaped}"

