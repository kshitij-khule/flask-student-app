from flask import Flask
from flask_cors import CORS
from .config import Config
import psycopg2
import os


def init_db():
    """Create tables if they don't exist. Runs once when app starts."""
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id   SERIAL PRIMARY KEY,
            name TEXT   NOT NULL,
            age  INT    NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def create_app():
    """
    App factory function.
    Instead of creating the Flask app at module level,
    we create it inside a function and return it.
    This makes testing easier and avoids circular imports.
    """
    app = Flask(__name__)
    
    # Load config
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app)

    # initialise database once — not per worker
    init_db()
    
    # Register blueprints (routes)
    # We'll uncomment these as we create each route file
    from .routes.students import students_bp
    app.register_blueprint(students_bp)
    
    return app