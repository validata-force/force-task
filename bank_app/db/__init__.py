import os
import sqlite3
from .models import db

def get_db_connection_string():
    """
    the connection string for the SQLite database
    """
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'bank.db')
    return f"sqlite:///{db_path}"

def init_app(app):
    """
    the database with the Flask app
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_connection_string()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

def create_tables():
    """
    directly the database tables if they do not exist
    """
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'bank.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS banks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()
