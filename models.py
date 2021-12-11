from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database"""
    db.app = app 
    db.init_app(app)
    
# Feedback Model 
class Feedback(db.Model):
    """Defines Feedback instance"""
    
    __tablename__ = "feedback"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    username = db.Column(db.String(50), db.ForeignKey("users.username"))
    
# User Model 
class User(db.Model):
    """Defines a user instance"""
    
    __tablename__ = "users"
    
    @classmethod 
    def register(cls, username, password):
        """Register user w/hashed password & return user."""
        
        hashed = bcrypt.generate_password_hash(password)
        
        # turn bytestring into normal (unicode utf8) string 
        hashed_utf8 = hashed.decode("utf8")
        
        # return instance of user w/username and hashed password 
        return cls(username=username, password=hashed_utf8)
        
    @classmethod 
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct."""
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            return user 
        else:
            return False 
        
        
    username = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    
    feedback = db.relationship('Feedback', backref="users", cascade="all")
    