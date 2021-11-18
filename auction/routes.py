from flask import flash, Blueprint, request, render_template, url_for, redirect
from .database_models import User # imports user class

#ensures no passwords are stored as plain text
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from flask_login import login_user, login_required, logout_user, current_user # login management modules

routes = Blueprint("routes", __name__) # blueprint allows splitting up routes over several files

@routes.route("/")
@login_required # requires the user to be logged in to access
def home_page():
    return render_template("home_page.html", user=current_user) # passes the current user to check there is someone signed in

@routes.route("/login", methods=['GET', 'POST'])
def login(): # users can login to the website using an existing account
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email = email).first() # checks all the users with the email entered
        
        if user: # if there is an existing user with the corresponding email
            if check_password_hash(user.password, password): # hashes password and checks it against the one in the database
                flash("You are now signed in", category="success")
                login_user(user, remember=True) # remembers the user is logged while the web server is using
                return redirect(url_for('routes.home_page')) # redirects the user to the home page
            else:
                flash("Password incorrect", category="warning")
        else:
            flash("Account does not exist", category="warning")
            
    return render_template("login.html", user=current_user)

@routes.route("/register", methods=['GET', 'POST'])
def register(): # users can register for a new account, saves new user to the database
    if request.method == 'POST':
        email = request.form.get("email") # gets data from the form
        firstname = request.form.get("firstname")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        
        user = User.query.filter_by(email = email).first() # checks all the users with the email entered
        if user: # if user already exists
            flash("Email used on another account.", category = "warning")
            
        elif password != confirm:
            flash("Both passwords must be the same", category = "warning")
        
        elif len(password) <= 5:
            flash("Password must be > 5 characters", category = "warning")
        
        else: #add new user to the database
            #creates a new User object, and applies a hashing algorithm to the password
            new_user = User(email=email, firstname=firstname, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit() # commits the new user
            
            login_user(new_user, remember=True) # logs in the new user
            flash("Account created.", category="success")
            return redirect(url_for('routes.home_page'))
    
    return render_template("register.html", user=current_user)

@routes.route("/logout")
@login_required
def logout():
    logout_user() # remembers that the user has logged out
    flash("You are now logged out.", category="success")
    return redirect(url_for("routes.login")) # redirects user back to the login page