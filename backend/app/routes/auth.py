# To store registrstion and login endpoints

import bcrypt
import jwt
import os
from datetime import datetime, timedelta, timezone
from flask import Blueprint, request, jsonify
from app.models.user import create_user, get_user_by_username

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

SECRET_KEY = os.environ.get("SECRET_KEY")


# ── Register ─────────────────────────────────────────
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # basic validation
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    # check if username already exists
    existing_user = get_user_by_username(username)
    if existing_user:
        return jsonify({"error": "Username already taken"}), 409

    # hash the password — never store plain text
    # bcrypt.hashpw needs bytes, so we encode the string first
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # store in DB
    create_user(username, hashed.decode("utf-8"))

    return jsonify({"message": "User created successfully"}), 201


# ── Login ─────────────────────────────────────────────
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # find the user
    user = get_user_by_username(username)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
        # note: we say "invalid credentials" not "user not found"
        # never tell attackers whether the username exists or not

    # user row is (id, username, password_hash)
    stored_hash = user[2]

    # check password against stored hash
    # bcrypt.checkpw hashes the input and compares — never decrypts
    if not bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
        return jsonify({"error": "Invalid credentials"}), 401

    # password correct — generate JWT token
    payload = {
        "user_id": user[0],           # who this token belongs to
        "username": user[1],
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)  # expires in 24 hours
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return jsonify({
        "message": "Login successful",
        "token": token
    }), 200