from flask import Flask
from flask_cors import CORS
from .config import Config
import psycopg2
import os


def init_db():
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cur = conn.cursor()

    # pg_try_advisory_lock is a PostgreSQL feature
    # it gets a lock at the database level — only one process can hold it at a time
    # if another worker tries to run this simultaneously, it waits
    cur.execute("SELECT pg_try_advisory_lock(1)")
    locked = cur.fetchone()[0]

    if locked:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id   SERIAL PRIMARY KEY,
                name TEXT   NOT NULL,
                age  INT    NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id       SERIAL PRIMARY KEY,
                username TEXT   NOT NULL UNIQUE,
                password TEXT   NOT NULL
            )
        """)

        conn.commit()

        # release the lock so other processes can proceed
        cur.execute("SELECT pg_advisory_unlock(1)")

    cur.close()
    conn.close()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    init_db()

    from .routes.students import students_bp
    from .routes.auth import auth_bp

    app.register_blueprint(students_bp)
    app.register_blueprint(auth_bp)

    return app