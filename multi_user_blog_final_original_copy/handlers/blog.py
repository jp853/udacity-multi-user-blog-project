import webapp2

from template import *
from handlers.database import User

class BlogHandler(webapp2.RequestHandler):
    """ This class adds the methods needed for authentication """
    """ This class is the jinja request handler """

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    # adds cookie to user
    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    # remove cookie to logout user
    def logout(self):
        self.response.headers.add_header(
            'Set-Cookie',
            'user_id=; Path=/')

    # stores the cookie
    def set_secure_cookie(self, name, key):
        cookie_val = make_secure_key(key)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    # initialize() is not necessary since google app engine does this for us
    # initialize() checks to see if the user is logged in or not
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

    # checks to see if cookie is valid
    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_key(cookie_val)

class BlogFrontHandler(BlogHandler):
    """ This class renders the front page of the blog
        and limits to the 10 most recent posts """

    def get(self):
        posts = db.GqlQuery(
            "select * from Post order by created desc limit 10")

        self.render('front.html', posts=posts)