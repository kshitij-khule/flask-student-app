from flask import Flask
from flask_cors import CORS
from .config import Config
import psycopg2
import os


def init_db():
    # Skip database init if in testing mode
    if os.environ.get('TESTING'):
        return
    
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cur = conn.cursor()
    
    # ... rest of your init_db code stays the same