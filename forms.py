from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Email 

class RegisterUser(FlaskForm):
    """Form for registering new users"""
    
    username = StringField("Username", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[Email(), InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])

class LoginUser(FlaskForm):
    """Form for logging in returning users"""
    
    username = StringField("Username", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """Form for feedback"""
    
    title = StringField("Title", validators=[InputRequired()])
    content = StringField("Content", validators=[InputRequired()])