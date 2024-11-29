from flask import render_template, Blueprint
from flask_login import login_required, current_user


views = Blueprint("views", __name__)


@views.route("/", methods=["GET"])
@login_required
def home():
    return render_template("home.html", user=current_user)
