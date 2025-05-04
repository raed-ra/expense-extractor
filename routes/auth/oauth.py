# routes/auth/oauth.py

from flask import Blueprint

oauth_bp = Blueprint("oauth", __name__, url_prefix="/auth/oauth")

@oauth_bp.route("/google")
def login_with_google():
    return "OAuth login coming soon!"
