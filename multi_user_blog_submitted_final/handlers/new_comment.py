from google.appengine.ext import db
from handlers.blog import BlogHandler
from template import *
from models.comment import Comment

#CREATE comment
class AddCommentHandler(BlogHandler):
    """ This class CREATES a new comment for post_id """

    def get(self, post_id, user_id):
        if not self.user:
            self.render('/login')
        else:
            self.render("new-comment.html")

    def post(self, post_id, user_id):
        if not self.user:
            return

        content = self.request.get('content')

        user_name = self.user.name
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())

        c = Comment(parent=key, user_id=int(user_id), content=content, user_name=user_name)
        c.put()

        self.redirect('/' + post_id)