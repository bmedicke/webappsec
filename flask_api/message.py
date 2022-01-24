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

blueprint = Blueprint("message", __name__)


def message_post():
    """
    validates message and posts it on success

    redirects to index
    """
    error = None

    if g.user is None:
        error = "log in first"

    text = request.form["text"]
    if not text or text.isspace():
        error = "empty message"

    if error is not None:
        flash(error)

    else:
        db = get_db()
        # write message to database:
        db.execute(
            """
            INSERT INTO message (author_id, text)
            VALUES (?, ?)
            """,
            (g.user["id"], text),
        )
        db.commit()

    return redirect(url_for("message.index"))


@blueprint.route("/", methods=("GET", "POST"))
def index():
    """
    landing page, lists and sends messages

    returns html
    """
    if request.method == "POST":
        return message_post()

    else:
        db = get_db()
        messages = db.execute(
            """
            SELECT message.id, author_id, created, username, avatar, text
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
    """
    sends messages

    returns html
    """
    if request.method == "POST":
        return message_post()

    return render_template("message/create.html")


@blueprint.route("/delete/<int:id>", methods=("POST",))
@login_required
def delete(id):
    """
    deletes a message (if it exists and is owned by user)

    redirects to index
    """
    error = None
    db = get_db()

    message_author = db.execute(
        """
        SELECT *
        FROM message
        WHERE id = ?
        """,
        (id,),
    ).fetchone()

    # invalid message id:
    if message_author is None:
        error = "denied"

    else:
        # logged in user did not author message:
        if g.user["id"] != message_author["author_id"]:
            error = "denied"

    if error:
        flash(error)
    else:
        db.execute(
            """
            DELETE FROM message
            WHERE id = ?
            """,
            (id,),
        )
        db.commit()

    return redirect(url_for("message.index"))
