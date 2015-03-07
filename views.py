# -*- coding: UTF-8 -*-

import webapp2
import jinja2
import os
import logging
from google.appengine.api import mail
# import sendgrid


SMTPserver = 'smtp.sendgrid.net'
USERNAME = "salmanwahed"
PASSWORD = "smw@$endGrid"
destination = ['salman2312@gmail.com']
text_subtype = 'plain'

logging.getLogger().setLevel(logging.DEBUG)
file_loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'blog'))

env = jinja2.Environment(
    loader=file_loader,
    extensions=["jinja2.ext.autoescape"],
    autoescape=True
)


# def sendgrid_mail(name, email, phone, body):
#     sg = sendgrid.SendGridClient(USERNAME, PASSWORD)
#     message = sendgrid.Mail()
#     message.add_to('Salman Wahed <salman2312@gmail.com>')
#     message.set_subject("Portfolio- Name: {} Phone: {}".format(name, phone))
#     message.set_html(body)
#     message.set_text(body)
#     message.set_from("{} {}".format(name, email))
#     status, msg = sg.send(message)
#     logging.info(status)
#     return True



def google_mail(name, email, phone, body):
    message = mail.EmailMessage(sender="<{}>".format(email),
                                 subject="Portfolio - Name:{} Phone:{}".format(name, phone))
    message.to = "Salman Wahed <salman2312@gmail.com>"
    message.body = body
    message.send()
    return True


class MyBlog(webapp2.RequestHandler):
    def get(self):
        logging.info("##get call")
        template = env.get_template('index.html')
        self.response.write(template.render())

    def post(self):
        name = self.request.get('name')
        logging.info("Name: %s" % name)

        email = self.request.get('email')
        logging.info("Email: %s" % email)

        phone = self.request.get('phone')
        logging.info("Phone: %s" % phone)

        message = self.request.get('message')
        logging.info("Message: %s" % message)

        # sendgrid_mail(name, email, phone, message)
        google_mail(name, email, phone, message)



application = webapp2.WSGIApplication(
    routes=[
        ('/', MyBlog),
    ],
    debug=True
)


# def main():
# webapp2.util.run_wsgi_app(application)
#
#
# if __name__ == '__main__':
#     main()