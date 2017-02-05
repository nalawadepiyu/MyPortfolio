#import statements
import os
import webapp2
import jinja2
import time
import logging
import re

from google.appengine.api import mail

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), \
                              autoescape=True)


EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class HomeHandler(BlogHandler):
    def get(self):
        self.render("portfolio.html")



class ContactMeHandler(BlogHandler):
    def post(self):
        print "post"
        email = self.request.get('email')
        name = self.request.get('name')
        message = self.request.get('message')

        if email and name and message:
            print "if"
            message = mail.EmailMessage(
                sender="Contact Me @ <piyu1081991@gmail.com>",
                subject="Contact Me")

            message.to = "Priyanka Nalawde <piyu1081991@gmail.com>",

            message.html = """
                <html><head></head><body>
                Message: %s
                <br>
                From: %s
                <br>
                </body></html>
                """ % (message, email)
            message.send()
            print "works"
            self.redirect('/#contact')

app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/contact', ContactMeHandler)
], debug=True)
