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

blueprint = Blueprint("profile", __name__)

# TODO: delete profile
# TODO: change password
# TODO: avatar as blob


@blueprint.route("/profile")
@login_required
def profile():
    """
    displays (logged in) user profile
    """
    return render_template("profile/show.html")


@blueprint.route("/edit", methods=("GET", "POST"))
@login_required
def edit():
    """
    allows logged in users to edit their profile
    """
    if request.method == "GET":
        return render_template("profile/edit.html")
    elif request.method == "POST":
        avatar = request.form["avatar"]
        private = bool(request.form.get("private"))

        db = get_db()
        # TODO: error handling!
        # TODO: sanitzie avatar!
        # TODO: chose avatar from list?
        # TODO: add exception handling!
        db.execute(
            "UPDATE user SET avatar = ?, private = ? WHERE id = ?",
            (avatar, private, g.user["id"]),
        )
        db.commit()
        return redirect(url_for("profile.profile"))
