from dotenv import load_dotenv
from flask import Flask, escape
import os


def create_app(test_config=None):
    '''
    application factory function for the Flask app.

    returns a Flask object
    '''
    # create a flask instance with config files relative to this file:
    # SECRET_KEY should be overwritten with a random value when deploying!
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
            )

    if test_config is None:
        # load app config:
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load test config:
        app.config.from_mapping(test_config)

    # create isntance folder for the sqlite db (if it's not already existing):
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


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


    @app.route("/e/<escaped>")
    def no_injection(escaped):
        """
        injection-safe demo route

        localhost:7701/e/<body onload='alert("this is bad");'>
        """
        return f"{escape(escaped)}"


    @app.route("/i/<unescaped>")
    def injection(unescaped):
        """
        injection demo route

        localhost:7701/i/<body onload='alert("this is bad");'>
        """
        return f"{unescaped}"


    return app
