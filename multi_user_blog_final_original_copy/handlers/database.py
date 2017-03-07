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

#define the Post class
class Post(db.Model):
    """ This class lists all the blog properties """
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    user_id = db.IntegerProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    likes = db.IntegerProperty(default=0)

    def render(self, current_user_id):
        key = db.Key.from_path('User', int(self.user_id), parent=users_key())
        user = db.get(key)

        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p=self, current_user_id=current_user_id, author=user.name)

    @classmethod
    def by_id(cls, uid):
        return Post.get_by_id(uid, parent=blog_key())

class Like(db.Model):
    """ This class stores 'likes' """
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    user_id = db.IntegerProperty(required=True)
    post_id = db.IntegerProperty(required=True)

class Comment(db.Model):
    """ This class stores the comments """
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    user_id = db.IntegerProperty(required=True)
    user_name = db.TextProperty(required=True)
