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
