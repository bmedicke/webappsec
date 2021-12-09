from dotenv import load_dotenv
from flask import Flask, escape

app = Flask(__name__)


@app.route("/")
def index():
    """
    landing page
    """
    return "<p>hello, world!</p>"


@app.route("/u/<user_id>")
def user_profile(user_id):
    """
    user profile page
    """
    return f"{escape(user_id)}'s profile"


@app.route("/i/<unescaped>")
def injection(unescaped):
    """
    injection demo route

    localhost:7701/i/<body onload='alert("this is bad");'>
    """
    return f"{unescaped}"
