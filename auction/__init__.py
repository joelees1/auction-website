from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager # manages logging in

db = SQLAlchemy() # defines a new database
DB_NAME = "database.db"

def app(): # creates and initialises a flask app
        
    app = Flask(__name__) # initializes the app
    app.secret_key = "password" # encrypts cookies and session data for the website
    
    # stores sqlite database in the current directory
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    db.init_app(app) # initialises database with the app
    
    # sets where uploaded images are saved
    app.config["IMAGE_UPLOADS"] = "/home/codio/workspace/auction/static/images"
    
    from .routes import routes # imports the routes from the route file
    app.register_blueprint(routes, url_prefix="/")
        
    from .database_models import Item, User # imports the database classes from the database_models file
    create_db(app)
    
    login_manager = LoginManager()
    login_manager.login_view = "routes.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id): # tells user how to find a user
        return User.query.get(int(id)) # looks for primary key, checking against the id passed
    
    return app

def create_db(app):
    # checks if the database exists already, creating it if not
    #if not path.exists("auction/" + DB_NAME): # determines if database.db is a path in the directory
    db.create_all(app=app) # creates the database