from google.appengine.ext import db
from handlers.blog import BlogHandler
from template import *

#DESTROY post
class DeletePostHandler(BlogHandler):
    """ This class DESTROYS the post """

    # can only delete by author
    def get(self, post_id, post_user_id):
        if self.user and self.user.key().id() == int(post_user_id):
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            post.delete()

            self.redirect('/')

        elif not self.user:
            self.redirect('/login')

        else:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)

            comments = db.GqlQuery(
                "select * from Comment where ancestor is :1 order by created desc limit 10", key)

            error = "You don't have permission to delete this post"
            self.render("permalink.html", post=post, comments=comments, error=error)