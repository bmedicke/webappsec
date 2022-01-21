from flask import Blueprint, flash, g, render_template, request, url_for
from flask_api.auth import login_required
from flask_api.database import get_db
from werkzeug.exceptions import abort

blueprint = Blueprint("profile", __name__)


@blueprint.route("/")
def index():
    """
    landing page
    """
    return render_template("index.html")
