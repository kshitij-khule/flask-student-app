"""
Mini project to understand backend systems:
client → HTTP → Flask → API → data → response

v2: Replaced in-memory list with SQLite database (raw SQL)
"""
import sqlite3
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- Database setup ---
# This is the path to the SQLite file
# SQLite is just a single .db file sitting on disk — no server needed
DATABASE = os.environ.get("DATABASE_PATH", "data/students.db")


def get_db():
    """Open a connection to the database."""
    conn = sqlite3.connect(DATABASE)
    # This makes rows behave like dictionaries
    # so you can do row["name"] instead of row[0]
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the students table if it doesn't exist yet."""
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


# Run once when the app starts — creates the table if missing
init_db()


# --- Routes ---

@app.route("/")
def home():
    return "Student server is running"


# GET → fetch all students
@app.route("/students", methods=["GET"])
def get_students():
    conn = get_db()
    rows = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    # each row is sqlite3.Row — convert to plain dict for jsonify
    return jsonify([dict(row) for row in rows])


# POST → add a new student
@app.route("/students", methods=["POST"])
def add_student():
    data = request.json
    conn = get_db()
    conn.execute(
        "INSERT INTO students (name, age) VALUES (?, ?)",
        (data["name"], data["age"])   # ? placeholders prevent SQL injection
    )
    conn.commit()
    conn.close()
    return jsonify({
        "message": "Student added",
        "data": data
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)