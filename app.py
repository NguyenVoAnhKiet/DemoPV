from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///D:/Zalo/DemoPV/Database/DemoDB"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


# Create the database
with app.app_context():
    db.create_all()


# Validation Functions
def is_valid_password(password):
    return (
        8 <= len(password) <= 40
        and any(c.isupper() for c in password)
        and any(c.islower() for c in password)
        and any(c.isdigit() for c in password)
        and any(c in "!@#$%^&*()_+[]{}|;:'\",.<>?/`~" for c in password)
    )


def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


# Routes
@app.route("/")
def home():
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if not username or not email or not password:
            return jsonify({"error": "All fields are required."}), 400

        if not is_valid_email(email):
            return jsonify({"error": "Invalid email address."}), 400

        if not is_valid_password(password):
            return (
                jsonify(
                    {
                        "error": "Password must be 8-40 characters long and include uppercase, lowercase, digits, and special characters."
                    }
                ),
                400,
            )

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User  registered successfully."}), 201

    return render_template("signup.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return jsonify({"message": "Login successful."}), 200

    return jsonify({"error": "Invalid email or password."}), 401


if __name__ == "__main__":
    app.run(debug=True)
