from handlers.blog import BlogHandler
from models.like import Like
from template import *

from google.appengine.ext import db

class LikePostHandler(BlogHandler):
    """ This class will add a 'like' to the post
        and will render an error if the original
        author likes own post  """

    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        if not post:
            return self.redirect('login')
        if self.user and self.user.key().id() == post.user_id:
            error = "Sorry, you cannot like your own post."
            self.render('base.html', access_error=error)
        elif not self.user:
            error = "You must be signed in to like a post."
            self.redirect('/login')
        else:
            user_id = self.user.key().id()
            post_id = post.key().id()

            like = Like.all().filter('user_id =', user_id).filter('post_id =', post_id).get()

            if like:
                self.redirect('/' + str(post.key().id()))

            else:
                like = Like(parent=key,
                            user_id=self.user.key().id(),
                            post_id=post.key().id())

                post.likes += 1

                like.put()
                post.put()

                self.redirect('/' + str(post.key().id()))