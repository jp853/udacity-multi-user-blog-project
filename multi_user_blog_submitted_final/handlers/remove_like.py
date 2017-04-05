from google.appengine.ext import db
from handlers.blog import BlogHandler
from template import *
from models.like import Like

class UnlikePostHandler(BlogHandler):
    """ This removes the like and
        class checks for errors """

    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        if not post:
            return self.redirect('login')
        if self.user and self.user.key().id() == post.user_id:
            self.write("You cannot dislike your own post")
        elif not self.user:
            self.redirect('/login')
        else:
            user_id = self.user.key().id()
            post_id = post.key().id()

            l = Like.all().filter('user_id =', user_id).filter('post_id =', post_id).get()

            if l:
                l.delete()
                post.likes -= 1
                post.put()

                self.redirect('/' + str(post.key().id()))
            else:
                self.redirect('/' + str(post.key().id()))