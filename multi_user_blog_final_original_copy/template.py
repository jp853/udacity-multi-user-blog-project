import hashlib
import hmac
import os
import random
import re
from string import letters

from google.appengine.ext import db

import jinja2

# Jinja configuration
# template loading code

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

# Parents

def users_key(group='default'):
    return db.Key.from_path('users', group)

def blog_key(name='default'):
    return db.Key.from_path('blogs', name)

secret = 'udacity'

# validate username, password, email
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

# make a key to save in a cookie with salt
def make_secure_key(key):
    return '%s|%s' % (key, hmac.new(secret, key).hexdigest())

# checks value of first and second key
# if not, return none
def check_secure_key(secure_key):
    key = secure_key.split('|')[0]
    if secure_key == make_secure_key(key):
        return key

# make a salt with 5 random letters
def make_salt(size=5):
    return ''.join(random.choice(letters) for x in xrange(size))

# make a hashed password
def make_pw_hash(username, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(username + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

# check hashed password
def valid_pw(username, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(username, password, salt)