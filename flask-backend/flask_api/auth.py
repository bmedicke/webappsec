from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_api.database import get_db
from werkzeug.security import check_password_hash, generate_password_hash
import functools

# auth blueprint to group views and related code:
blueprint = Blueprint("auth", __name__, url_prefix="/auth")


# handle /auth/register:
@blueprint.route("/register", methods=("GET", "POST"))
def register():
    """
    register blueprint

    returns html
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        error = None

        if not username:
            error = "Username can not be empty"

        if not password:
            error = "Password can not be empty"

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()  # write to db.

            except db.IntegrityError:
                error = f"Username {username} already taken."
            else:
                # generate url to avoid hardcoding:
                return redirect(url_for("auth.login"))

            flash(error)

    return render_template("auth/register.html")


@blueprint.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        # TODO: don't leak info!
        if user is None:
            error = "invalid credentials (user)"
        elif not check_password_hash(user["password"], password):
            error = "invalid credentials (pass)"

        if error is None:
            session.clear()  # clear session dict.
            # flask signs the cookie data!
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")
