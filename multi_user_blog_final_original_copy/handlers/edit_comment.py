from google.appengine.ext import db
from handlers.blog import BlogHandler
from template import *

#UPDATE Comment
class EditCommentHandler(BlogHandler):
    """ This class UPDATES the edit comment page """

    def get(self, post_id, post_user_id, comment_id):
        if self.user and self.user.key().id() == int(post_user_id):
            postkey = db.Key.from_path('Post', int(post_id), parent=blog_key())
            key = db.Key.from_path('Comment', int(comment_id), parent=postkey)
            comment = db.get(key)

            self.render('edit-comment.html', content=comment.content)

        elif not self.user:
            self.redirect('/login')

        else:
            self.write("You don't have permission to edit this comment.")

    #only original author can update comment
    def post(self, post_id, post_user_id, comment_id):
        if not self.user:
            return

        if self.user and self.user.key().id() == int(post_user_id):
            content = self.request.get('content')

            postkey = db.Key.from_path('Post', int(post_id), parent=blog_key())
            key = db.Key.from_path('Comment', int(comment_id), parent=postkey)
            comment = db.get(key)

            comment.content = content
            comment.put()

            self.redirect('/' + post_id)

        else:
            self.write("You don't have permission to edit this comment.")