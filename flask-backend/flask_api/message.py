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


def message_post():
    error = None

    if g.user is None:
        error = "log in first"

    text = request.form["text"]
    if not text:
        error = "empty message"

    if error is not None:
        flash(error)
        return redirect(url_for("index"))

    else:
        db = get_db()
        db.execute(
            """
            INSERT INTO message (author_id, text)
            VALUES (?, ?)
            """,
            (g.user["id"], text),
        )
        db.commit()
        return redirect(url_for("index"))


@blueprint.route("/", methods=("GET", "POST"))
def index():
    """
    landing page
    """
    if request.method == "POST":
        return message_post()

    else:
        db = get_db()
        messages = db.execute(
            """
            SELECT author_id, created, username, avatar, text
            FROM message
            JOIN user
            ON message.author_id = user.id
            ORDER BY created ASC
            """
        ).fetchall()

        return render_template("index.html", messages=messages)


@blueprint.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        return message_post()

    return render_template("message/create.html")
