from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    db.app = app 
    db.init_app(app)
    
# User Model 
class User(db.Model):
    """Defines a user instance"""
    username = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    