from webapp2 import WSGIApplication
from google.appengine.ext import db
import template

import handlers.database
from handlers.blog import BlogHandler, BlogFrontHandler
from handlers.auth import SignupHandler, LoginHandler, LogoutHandler
from handlers.new_post import NewPostHandler
from handlers.edit_post import EditPostHandler
from handlers.post import PostHandler
from handlers.remove_post import DeletePostHandler
from handlers.like import LikePostHandler
from handlers.remove_like import UnlikePostHandler
from handlers.new_comment import AddCommentHandler
from handlers.edit_comment import EditCommentHandler
from handlers.remove_comment import DeleteCommentHandler

app = WSGIApplication([
    ('/', BlogFrontHandler),
    ('/signup', SignupHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/newpost', NewPostHandler),
    ('/([0-9]+)', PostHandler),
    ('/([0-9]+)/like', LikePostHandler),
    ('/([0-9]+)/unlike', UnlikePostHandler),
    ('/([0-9]+)/edit', EditPostHandler),
    ('/([0-9]+)/delete/([0-9]+)', DeletePostHandler),
    ('/([0-9]+)/addcomment/([0-9]+)', AddCommentHandler),
    ('/([0-9]+)/([0-9]+)/editcomment/([0-9]+)', EditCommentHandler),
    ('/([0-9]+)/([0-9]+)/deletecomment/([0-9]+)', DeleteCommentHandler)
], debug=True)
