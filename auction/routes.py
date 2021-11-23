from flask import flash, Blueprint, request, render_template, url_for, redirect
from .database_models import User, Item # imports user and item class
#ensures no passwords are stored as plain text
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename # allows me to change the uploaded files name
from . import db
from flask_login import login_user, login_required, logout_user, current_user # login management modules
import os


routes = Blueprint("routes", __name__) # blueprint allows splitting up routes over several files

# sets where uploaded images are saved and which image extensions are allowed
UPLOAD_FOLDER = "/home/codio/workspace/auction/static/images"
ALLOWED_EXTENSIONS = set(['jpg'])

@routes.route("/", methods=['GET', 'POST'])
@login_required # requires the user to be logged in to access
def home_page():
    items = Item.query.all() # gets all rows of items
    users = User.query.all() # gets all rows of items
    return render_template("home_page.html", items=items, user=current_user, users=users, extensions=ALLOWED_EXTENSIONS) # sends items to the html and keeps track of login status

@routes.route("/login", methods=['GET', 'POST'])
def login(): # users can login to the website using an existing account
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email = email).first() # checks all the users with the email entered
        
        if user: # if there is an existing user with the corresponding email
            if check_password_hash(user.password, password): # hashes password and checks it against the one in the database
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
        phone = request.form.get("phone")
        username = request.form.get("username")
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
            new_user = User(email=email, phone=phone, username=username, password=generate_password_hash(password, method='sha256'))
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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# ********adds to the database even with the wrong extension, since it needs to commit to get user id*************
@routes.route("/sell", methods=['GET', 'POST'])
@login_required
def sell(): # user can enter information about an item they would like to add to the home page in order to sell
    if request.method == 'POST':
        item_name = request.form.get("item_name") # forms gather information
        item_name = item_name.capitalize() # capitalizes name
        description = request.form.get("description")
        description = description.capitalize()
        start_bid = request.form.get("start_bid")

        #creates a new Item object
        new_item = Item(item_name=item_name, description=description, start_bid=start_bid, user_id=current_user.id)
        db.session.add(new_item)
        db.session.commit() # commits the new item to the database
            
        item_id = new_item.item_id # gets the current items id
            
        if request.files: # if a file is sent, saves it to the item_image variable
            item_image = request.files["item_image"] # gets the file from the form
                
            if allowed_file(item_image.filename): # only allows the file input, and commits to the database, if the image is .jpg
                # saves image to the default directory given in the init file, as item_id.fileextension
                filename = secure_filename(str(item_id) + ".jpg") # + '.' + item_image.filename.rsplit('.', 1)[1] for other filetypes
                item_image.save(os.path.join(UPLOAD_FOLDER, filename)) # saves the file to the specified upload folder
                
                flash("Item added.", category="success")
                return redirect(url_for('routes.home_page')) # once item is created redirects to the home page
                
            else:
                flash("Invalid filetype.", category="warning")
                
                # if the file uploaded is not a jpg, remove the item from the database
                Item.query.filter_by(item_id=item_id).delete()
                db.session.commit()
        
    return render_template("sell.html", user=current_user)

@routes.route("/myitems", methods=['GET', 'POST'])
@login_required
def my_items(): # shows items the user has for put sale
    length = len(current_user.items) # how many items the user has for sale
    if length > 0:
        return render_template("my_items.html", user=current_user) # shows the user their items
    else:
        return render_template("no_items.html", user=current_user) # tells the user they have nothing for sale
    
    
@routes.route("/item/<int:item_id>", methods=['GET', 'POST'])
@login_required
def item_info(item_id): # route shows users a dedicated page for each item, with all its information
    user = current_user
    users = User.query.all() # gets all users
    item = Item.query.filter_by(item_id=item_id).first() # finds the item the user clicked ons information
    return render_template("item.html", user=current_user, users=users, item=item)

@routes.route("/delete/<int:item_id>", methods=['GET', 'POST'])
@login_required
def item_delete(item_id): # allows a user to delete their item from the website
    user=current_user
    item = Item.query.filter_by(item_id=item_id).first() # finds the item they clicked on
    
    # prevents another user deleting items they don't own
    if item.user_id == user.id: # if the current user is the items owner
        Item.query.filter_by(item_id=item_id).delete() # deletes the item
        db.session.commit()
        flash("Item deleted", category="success")
    
    else:
        flash("Unauthorised user", category="warning") # tells the user if they try to delete someone elses item
        
    return redirect(url_for('routes.home_page')) # redirects to the home page

@routes.route("/sold/<int:item_id>", methods=['GET', 'POST'])
@login_required
def sold(item_id): # allows a user to mark an item as sold
    user=current_user
    item = Item.query.filter_by(item_id=item_id).first() # finds the item they want to mark
    
    # prevents another user marking items they don't own
    if item.user_id == user.id: # if the current user is the items owner
        item.sold = True
        db.session.commit()
    
    else:
        flash("Unauthorised user", category="warning") # tells the user if they try to delete someone elses item
        
    return redirect(url_for('routes.my_items')) # redirects to the home page