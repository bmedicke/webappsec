from flask import (
    Blueprint,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_api.auth import login_required
from flask_api.database import get_db
from glob import glob
import os

blueprint = Blueprint("profile", __name__)

# TODO: allow user to delete the profile
# TODO: allow user to change the password


def profile_pic(basename):
    """
    returns relative path to profile picture
    """
    return url_for("static", filename="profiles/" + basename + ".png")


@blueprint.route("/profile")
@login_required
def profile():
    """
    displays (logged in) user profile

    returns html
    """
    return render_template("profile/show.html")


def get_profile_pics():
    """
    gets names of available profile pics

    returns list of basenames without file ending
    """
    profiles_path = url_for("static", filename="profiles")
    files = glob(
        os.path.join(current_app.root_path + profiles_path + "/*.png")
    )
    profile_pics = list()

    for file in files:
        profile_pics.append(os.path.basename(file.strip(".png")))

    return profile_pics


@blueprint.route("/profile/edit", methods=("GET", "POST"))
@login_required
def edit():
    """
    allows logged in users to edit their profile

    returns html
    """
    if request.method == "GET":
        return render_template(
            "profile/edit.html", profile_pics=get_profile_pics()
        )

    elif request.method == "POST":
        error = None

        about = request.form["about"]
        private = bool(request.form.get("private"))
        avatar = request.form["avatar"]

        if avatar not in get_profile_pics():
            error = "invalid profile picture choice"

        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                """
                UPDATE user
                SET avatar = ?, private = ?, about = ?
                WHERE id = ?
                """,
                (avatar, private, about, g.user["id"]),
            )
            db.commit()

        return redirect(url_for("profile.profile"))


# TODO: escape this endpoint?
@blueprint.route("/user/<int:id>")
def user(id):
    """
    shows profile of user by id (if set to public)

    return html
    """
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
