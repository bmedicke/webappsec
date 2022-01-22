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
from glob import glob
from werkzeug.exceptions import abort
import os

blueprint = Blueprint("profile", __name__)

# TODO: delete profile
# TODO: change password


@blueprint.route("/profile")
@login_required
def profile():
    """
    displays (logged in) user profile
    """
    return render_template("profile/show.html")


@blueprint.route("/profile/edit", methods=("GET", "POST"))
@login_required
def edit():
    """
    allows logged in users to edit their profile
    """
    if request.method == "GET":
        cwd = os.path.join(os.getcwd() + "/flask_api")
        relpath = url_for("static", filename="profiles")
        files = glob(os.path.join(cwd + relpath + "/*.png"))
        profile_pics = list()

        for file in files:
            profile_pics.append(os.path.basename(file.strip(".png")))

        return render_template("profile/edit.html", profile_pics=profile_pics)

    elif request.method == "POST":
        avatar = request.form["avatar"]
        about = request.form["about"]
        private = bool(request.form.get("private"))

        db = get_db()
        # TODO: error handling!
        # TODO: add exception handling!
        db.execute(
            """
            UPDATE user
            SET avatar = ?, private = ?, about = ?
            WHERE id = ?""",
            (avatar, private, about, g.user["id"]),
        )
        db.commit()
        return redirect(url_for("profile.profile"))


@blueprint.route("/user/<int:id>")
def user(id):
    db = get_db()
    user = db.execute(
        """
        SELECT username, private, avatar, about
        FROM user
        WHERE id = ?
        """,
        (id,),
    ).fetchone()

    return render_template("/profile/user.html", user=user)
