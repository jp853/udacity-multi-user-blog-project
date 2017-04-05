#this file contains the elements that are stored in the database
from google.appengine.ext import db
from template import *

class Comment(db.Model):
    """ This class stores the comments """
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    user_id = db.IntegerProperty(required=True)
    user_name = db.TextProperty(required=True)