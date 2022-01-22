from flask import (
    Blueprint,
    flash,
    g,
    render_template,
    request,
    url_for,
    redirect,
)
from flask_api.auth import login_required
from flask_api.database import get_db
from werkzeug.exceptions import abort

blueprint = Blueprint("message", __name__)


@blueprint.route("/")
def index():
    """
    landing page
    TODO: add list of profiles
    """
    return render_template("index.html")
