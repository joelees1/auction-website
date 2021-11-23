from . import db # imports db from the current folder
from flask_login import UserMixin
from sqlalchemy.sql import func

class Item(db.Model): # class that stores info about each item on the system
    item_id = db.Column(db.Integer, primary_key=True) # primary key id number
    item_name = db.Column(db.String(150))
    description = db.Column(db.String(500))
    start_bid = db.Column(db.Integer)
    item_image = db.Column(db.Text())

    date_only = db.Column(db.Date, server_default=func.date()) # just the date the item was made
    date = db.Column(db.DateTime(timezone=True), server_default=func.now()) # defaults the datetime to now
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # must pass a valid id of an existing user to this object, 1 to many

class User(db.Model, UserMixin): # creates each user in the database
    id = db.Column(db.Integer, primary_key=True) # primary key id number
    email = db.Column(db.String(150)) # max email length 150 characters
    phone = db.Column(db.Integer)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    items = db.relationship('Item') # a list of all the items a user owns

#current_bid = db.Column(db.Integer)