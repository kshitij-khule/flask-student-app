from flask import Flask
from flask_cors import CORS
from .config import Config

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
    
    # Register blueprints (routes)
    # We'll uncomment these as we create each route file
    from .routes.students import students_bp
    app.register_blueprint(students_bp)
    
    return app