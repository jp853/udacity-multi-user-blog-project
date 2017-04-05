#this file contains the elements that are stored in the database
from google.appengine.ext import db
from template import *

class Like(db.Model):
    """ This class stores 'likes' """
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    user_id = db.IntegerProperty(required=True)
    post_id = db.IntegerProperty(required=True)