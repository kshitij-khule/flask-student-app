# create user table if not exist and define database logicimport psycopg2
import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db():
    """Open a connection to PostgreSQL."""
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def init_users_table():
    """Create users table if it doesn't exist."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       SERIAL PRIMARY KEY,
            username TEXT   NOT NULL UNIQUE,  -- UNIQUE means no two users can have same username
            password TEXT   NOT NULL          -- stores the hash, not plain text
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


def create_user(username, hashed_password):
    """Insert a new user into the database."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, hashed_password)
    )
    conn.commit()
    cur.close()
    conn.close()


def get_user_by_username(username):
    """Find a user by username. Returns None if not found."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username = %s",
        (username,)
    )
    row = cur.fetchone()  # fetchone() returns one row or None
    cur.close()
    conn.close()
    return row


'''Why a separate `models/user.py`?*'''

'''
All database logic for users lives here. The routes file just calls these functions — it doesn't care how the database works. This is that separation of concerns again:

auth.py (route)     →  "give me the user with this username"
user.py (model)     →  "okay, here's how to get it from the DB" 

'''