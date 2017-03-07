from handlers.blog import BlogHandler
from handlers.database import Post
from template import *

#CREATE new blog post
class NewPostHandler(BlogHandler):
    """ This class CREATES a new blog post """
    def get(self):
        # Reads the form
        if self.user:
            self.render("new-post.html")
        else:
            error = "You must be signed in to create a post."
            self.render("base.html", access_error=error)

    # store blog post into database
    def post(self):
        if not self.user:
            return self.redirect('/login')

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent=blog_key(), subject=subject,
                     content=content, user_id=self.user.key().id())
            p.put()
            self.redirect('/%s' % str(p.key().id()))
        else:
            error = "Please fill up the fields."
            self.render("new-post.html", subject=subject,
                        content=content, error=error)