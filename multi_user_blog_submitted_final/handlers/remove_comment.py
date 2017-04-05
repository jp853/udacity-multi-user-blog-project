from google.appengine.ext import db
from handlers.blog import BlogHandler
from template import *

# DESTROY Comment
class DeleteCommentHandler(BlogHandler):
    """ This class DESTROYS the comment for post_id """

    def get(self, post_id, post_user_id, comment_id):
        postkey = db.Key.from_path('Post', int(post_id), parent=blog_key())
        key = db.Key.from_path('Comment', int(comment_id), parent=postkey)
        comment = db.get(key)
        if not comment:
            return self.redirect('login')
        if self.user and self.user.key().id() == comment.user_id:
            comment.delete()
            self.redirect('/' + post_id)
        elif not self.user:
            self.redirect('/')
        else:
            self.write("You don't have permission to delete this comment.")