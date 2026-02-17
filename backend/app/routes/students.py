import bcrypt
import jwt
import os
from functools import wraps
from flask import Blueprint, request, jsonify
import psycopg2
import psycopg2.extras

students_bp = Blueprint("students", __name__, url_prefix="/students")
DATABASE_URL = os.environ.get("DATABASE_URL")
SECRET_KEY = os.environ.get("SECRET_KEY")


def token_required(f):
    """
    Decorator that checks for a valid JWT token before allowing access.
    Usage: add @token_required above any route you want to protect.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # token comes in the header like:
        # Authorization: Bearer eyJhbGci...
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]  # get just the token part

        if not token:
            return jsonify({"error": "Token missing"}), 401

        try:
            # verify signature and expiry
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # attach user info to the request so the route can use it
            request.current_user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated


def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


@students_bp.route("/", methods=["GET"])
@token_required          # ← protected
def get_students():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(row) for row in rows])


@students_bp.route("/", methods=["POST"])
@token_required          # ← protected
def add_student():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, age) VALUES (%s, %s)",
        (data["name"], data["age"])
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Student added", "data": data})

'''
What is a decorator?

That `@token_required` above the route — it's a function that wraps another function. Think of it like a security guard standing in front of a door:

Request comes in
      ↓
token_required runs first  ← security guard checks wristband
      ↓ (if valid)
actual route runs          ← you get into the club
      ↓ (if invalid)
returns 401                ← bouncer turns you away

'''