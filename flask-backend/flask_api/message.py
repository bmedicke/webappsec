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


@blueprint.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        text = request.form["text"]
        author = g.user["id"]
        error = None

        if not text:
            error = "empty message"

        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                "INSERT INTO message (author_id, text)" "VALUES (?, ?)",
                (author, text),
            )
            db.commit()
            return redirect(url_for("message.create"))

    return render_template("message/create.html")
