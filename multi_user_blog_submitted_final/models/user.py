#this file contains the elements that are stored in the database
from google.appengine.ext import db
from template import *

class User(db.Model):
    """ this class is the user object that is stored in the database """
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True) #store hashed password
    email = db.StringProperty()

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent=users_key(),
                    name=name,
                    pw_hash=pw_hash,
                    email=email)

    # the decorators call methods on particular objects
    # looks up user by its name

    # checks if the user and password matches
    @classmethod
    def login(cls, username, password):
        u = User.by_name(username)
        if u and valid_pw(username, password, u.pw_hash):
            return u

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u