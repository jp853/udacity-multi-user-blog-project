from google.appengine.ext import db
from handlers.blog import BlogHandler
from template import *

# DESTROY Comment
class DeleteCommentHandler(BlogHandler):
    """ This class DESTROYS the comment for post_id """

    def get(self, post_id, post_user_id, comment_id):

        if self.user and self.user.key().id() == int(post_user_id):
            postkey = db.Key.from_path('Post', int(post_id), parent=blog_key())
            key = db.Key.from_path('Comment', int(comment_id), parent=postkey)
            comment = db.get(key)
            comment.delete()

            self.redirect('/' + post_id)

        elif not self.user:
            self.redirect('/login')

        else:
            self.write("You don't have permission to delete this comment.")