from handlers.blog import BlogHandler
from handlers.database import User
from template import *

class SignupHandler(BlogHandler):
    """ This class renders the signup page and
        redirects to the front page or redirect
        back to the sign up page if an error renders """

    #checks if there's an existing user, otherwise
    #stores in database
    def done(self):
        u = User.by_name(self.username)

        if u:
            error = 'That user already exists.'
            self.render('signup.html', error=error)

        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/')

    #renders signup page
    def get(self):
        self.render('signup.html')

    # redirects to front page if valid
    # if not valid, render sign up page with errors displayed
    def post(self):
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username=self.username,
                      email=self.email)

        if not valid_username(self.username):
            params['error'] = "That's not a valid username."
            return self.render('signup.html', **params)

        if not valid_password(self.password):
            params['error'] = "That wasn't a valid password."
            return self.render('signup.html', **params)

        elif self.password != self.verify:
            params['error'] = "Your passwords didn't match."
            return self.render('signup.html', **params)

        if not valid_email(self.email):
            params['error'] = "That's not a valid email."
            return self.render('signup.html', **params)

        self.done()

class LoginHandler(BlogHandler):
    """ This class logs the user in """

    # render login form if user is
    # not logged in
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)

        if u:
            self.login(u)
            self.redirect('/')
        else:
            error = 'Invalid Username or Password'
            self.render('login-form.html', error=error)

class LogoutHandler(BlogHandler):
    """ This class logs the user out """

    def get(self):
        self.logout()
        self.redirect('/')