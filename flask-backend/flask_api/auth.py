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
import functools  # for creating a decorator.

# auth blueprint to group views and related code:
blueprint = Blueprint("auth", __name__, url_prefix="/auth")


def validate_credentials(username, password, password_confirmation):
    """
    checks if password and username match requirements

    returns error or None
    """
    PASSWORD_MIN_LEN = 12
    error = None

    if not username:
        error = "username can not be empty"

    if not password:
        error = "password can not be empty"

    if len(password) < PASSWORD_MIN_LEN:
        error = f"password too short ({PASSWORD_MIN_LEN} chars minimum)"

    if password != password_confirmation:
        error = "passwords do not match"

    return error


# handle /auth/register:
@blueprint.route("/register", methods=("GET", "POST"))
def register():
    """
    allows creation of new users

    returns html
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_confirmation = request.form["password_confirmation"]

        error = validate_credentials(username, password, password_confirmation)

        if error is None:
            try:
                db = get_db()
                db.execute(
                    """
                    INSERT INTO user (username, password)
                    VALUES (?, ?)
                    """,
                    (username, generate_password_hash(password)),
                )
                db.commit()  # write to db.

            except db.IntegrityError:
                error = f"username {username} already taken."

        flash(error or "account created")

    return render_template("auth/register.html")


@blueprint.route("/login", methods=("GET", "POST"))
def login():
    """
    allows users to log in

    returns html
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            """
            SELECT *
            FROM user
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

        if user is None:
            error = "invalid credentials"
        elif not check_password_hash(user["password"], password):
            error = "invalid credentials"

        if error is None:
            session.clear()  # clear session dict.
            # flask signs the cookie data!
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@blueprint.before_app_request
def load_logged_in_user():
    """
    gets session data from cookie (if it exists)

    stores data in g object (for duration of request)
    """
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None

    else:
        g.user = (
            get_db()
            .execute(
                """
                SELECT *
                FROM user
                WHERE id = ?
                """,
                (user_id,),
            )
            .fetchone()
        )


@blueprint.route("/logout")
def logout():
    """
    destroys the current session and return user to index
    """
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    """
    decorator for views that require authentication

    returns view that redirects to login page if not logged in
    """

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
