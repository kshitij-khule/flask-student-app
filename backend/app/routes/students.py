import psycopg2
import psycopg2.extras
import os
from flask import Blueprint, request, jsonify

students_bp = Blueprint("students", __name__, url_prefix="/students")

# reads from env var — will be set by Docker Compose
DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db():
    """Open a connection to PostgreSQL."""
    conn = psycopg2.connect(DATABASE_URL)
    return conn




@students_bp.route("/", methods=["GET"])
def get_students():
    conn = get_db()
    # RealDictCursor makes rows behave like dicts — same as sqlite3.Row
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(row) for row in rows])


@students_bp.route("/", methods=["POST"])
def add_student():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, age) VALUES (%s, %s)",  # %s not ?
        (data["name"], data["age"])
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Student added", "data": data})