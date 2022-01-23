from dotenv import load_dotenv  # automatically load .flaskenv
from flask import Flask
from flask_wtf.csrf import CSRFProtect
import os


def create_app(test_config=None):
    """
    application factory function for the Flask app.

    returns a Flask object
    """

    # read secret key from env vars when deploying,
    # used for signing session cookies:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev")

    # name app after module name:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        DATABASE=os.path.join(app.instance_path, "flask-api.sqlite"),
    )

    if test_config is None:
        # load app config:
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load test config:
        app.config.from_mapping(test_config)

    # create instance folder for the sqlite db (if it's not already existing):
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register database functions with the app (includes cli command):
    from . import database

    database.init_app(app)

    # register authentication blueprint (register/login/logout):
    from . import auth

    app.register_blueprint(auth.blueprint)

    # register profile blueprint (show/edit):
    from . import profile

    app.register_blueprint(profile.blueprint)

    # register message blueprint (including index endpoint):
    from . import message

    app.register_blueprint(message.blueprint)
    app.add_url_rule("/", endpoint="index")

    # require valid CSRF token for modifying requests:
    csrf = CSRFProtect()
    csrf.init_app(app)

    return app
