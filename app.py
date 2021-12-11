from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension 
from models import db, connect_db, User, Feedback 
from forms import RegisterUser, LoginUser, FeedbackForm 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_ECHO'] = True 
app.config['SECRET_KEY'] = 'anothersecretanotherseason'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def redirect_to_register():
    """Redirects to Register Page"""
    return redirect('/register')
    
@app.route('/register', methods=["GET", "POST"])
def get_register_page():
    """Gets the Register Page"""
    form = RegisterUser()
    
    if form.validate_on_submit():
        # Get data from front-end
        username = form.username.data
        password = form.password.data
        email = form.email.data 
        first_name = form.first_name.data 
        last_name = form.last_name.data 
        
        # Save the data correctly in the database 
        newUser = User.register(username, password)
        newUser.email = email 
        newUser.first_name = first_name 
        newUser.last_name = last_name 
        
        # Check to see if username is already taken 
        check_user = User.query.filter_by(username=newUser.username).first()
        
        if check_user:
            return render_template("register.html", form=form, error="Username Already Taken")
        
        db.session.add(newUser)
        db.session.commit()
        
        # Save user into current session 
        session["user_id"] = newUser.username
        
        # Redirect to secret page 
        return redirect(f'/users/{newUser.username}')
    else:
        return render_template("register.html", form=form)
        
@app.route('/login', methods=["GET", "POST"])
def get_login_page():
    """Gets the Login Page"""
    form = LoginUser()
    
    if form.validate_on_submit():
        # Get data from front-end 
        username = form.username.data
        password = form.password.data
        
        # Attempt to authenticate user 
        user = User.authenticate(username, password)
        
        if user:
            # Save new user into current session 
            session["user_id"] = user.username
            
            # Redirect to secret page  
            return redirect(f'/users/{user.username}')
        else:
            return render_template("login.html", form=form, error="Wrong Password or Username")
    else:
        return render_template("login.html", form=form)
        
@app.route('/users/<username>')
def get_username_page(username):
    """Gets the username page"""
    
    if username != session["user_id"]:
        return redirect("/")
    else:
        # Get user from database 
        user = User.query.filter_by(username=username).first()
        return render_template("user.html", user=user)
        
@app.route('/logout')
def logout_users():
    """Logs out users"""
    
    session.pop("user_id")
    return redirect('/')

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """Deletes a user"""
    
    if username == session["user_id"]:
        User.query.filter_by(username=username).delete()
        return redirect("/")
    else:
        return redirect("/")
        
@app.route('/users/<username>/feedback/add', methods=["POST", "GET"])
def get_feedback_form(username):
    """Displays the feedback form"""
    form = FeedbackForm()
    
    if username == session["user_id"]:
        
        if form.validate_on_submit():
            title = form.title.data 
            content = form.content.data 
            
            newForm = Feedback(title=title, content=content, username=username)
            
            db.session.add(newForm)
            db.session.commit()
            
            return redirect(f'/users/{username}')
        else:
            return render_template("feedback_form.html", form=form)
    else:
        return redirect('/')
    
@app.route('/feedback/<feedbackId>/update', methods=["POST", "GET"])
def get_update_form(feedbackId):
    """Displays the feedback update form"""
    
    # Get the feedback object 
    feedback = Feedback.query.get(feedbackId)
    
    # Get the form 
    form = FeedbackForm(obj=feedback)
    
    if feedback.username == session["user_id"]:
        
        if form.validate_on_submit():
            updatedTitle = form.title.data 
            updatedContent = form.content.data 
            
            feedback.title = updatedTitle 
            feedback.content = updatedContent 
            
            db.session.add(feedback)
            db.session.commit()
            
            return redirect(f'/users/{feedback.username}')
        else:
            return render_template("update_feedback_form.html", form=form) 
    else:
        return redirect('/')
    
@app.route('/feedback/<feedbackId>/delete', methods=["POST", "GET"])
def delete_feedback(feedbackId):
    """Deletes a specified piece of feedback"""
    
    feedback = Feedback.query.get(feedbackId)
    
    if feedback.username == session["user_id"]:
        Feedback.query.filter_by(id=feedbackId).delete()
        db.session.commit()
        return redirect(f'/users/{session["user_id"]}')
    else:
        return redirect('/')
    
    
    