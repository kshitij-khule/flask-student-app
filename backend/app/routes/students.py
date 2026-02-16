import sqlite3
import os
from flask import Blueprint, request, jsonify

# A Blueprint is a mini Flask app — a group of related routes
# We register it in create_app() and Flask treats it as part of the main app
# url_prefix means all routes here start with /students
students_bp = Blueprint("students", __name__, url_prefix="/students")

DATABASE = os.environ.get("DATABASE_URL", "data/students.db")


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT    NOT NULL,
            age  INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()


@students_bp.route("/", methods=["GET"])
def get_students():
    conn = get_db()
    rows = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


@students_bp.route("/", methods=["POST"])
def add_student():
    data = request.json
    conn = get_db()
    conn.execute(
        "INSERT INTO students (name, age) VALUES (?, ?)",
        (data["name"], data["age"])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Student added", "data": data})


""""

**What is a Blueprint?**

Think of it like a section of a restaurant menu. The full menu is your Flask app. Each Blueprint is one section — starters, mains, desserts. Each section has its own items (routes) but they all belong to the same menu (app).
Flask app
├── students Blueprint  →  /students/
└── auth Blueprint      →  /auth/login, /auth/register  (coming soon)
"""