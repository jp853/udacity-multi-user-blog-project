from google.appengine.ext import db
from handlers.blog import BlogHandler
from template import *

#UPDATE post
class EditPostHandler(BlogHandler):
    """ This class UPDATES the post """

    def get(self, post_id):
        # Reads updated post
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        if not post:
            return self.redirect('login')
        if self.user and self.user.key().id() == post.user_id:
            self.render('edit-post.html', subject=post.subject,
                        content=post.content, post_id=post_id)

        elif not self.user:
            self.redirect('/login')

        else:
            self.write("You cannot edit this post becuase you are not the one who wrote this post.")

    #store post into database
    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not self.user:
            return self.redirect('/login')

        if self.user and self.user.key().id() == post.user_id:
            subject = self.request.get('subject')
            content = self.request.get('content')

            if subject and content:
                key = db.Key.from_path('Post', int(post_id), parent=blog_key())
                post = db.get(key)

                post.subject = subject
                post.content = content

                post.put()

                self.redirect('/%s' % str(post.key().id()))
            else:
                error = "subject and content, please!"
                self.render("new-post.html", subject=subject,
                            content=content, error=error)

        else:
            self.write("You cannot edit this post becuase you are not the one who wrote this post.")