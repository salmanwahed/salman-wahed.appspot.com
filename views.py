# -*- coding: UTF-8 -*-

import os
import logging
import webapp2
import jinja2
import sendgrid
import settings


logging.getLogger().setLevel(logging.DEBUG)
file_loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'blog'))

env = jinja2.Environment(
    loader=file_loader,
    extensions=["jinja2.ext.autoescape"],
    autoescape=True
)


def sendgrid_mail(name, email, phone, body):
    sg = sendgrid.SendGridClient(settings.USERNAME, settings.PASSWORD)
    message = sendgrid.Mail()
    message.add_to(settings.TO_ADDRESS)
    body = body + "<br /><br /><strong>Name:</strong> {name} <br />" \
                  "<strong>Phone:</strong> <i>{phone}<i>".format(name=name, phone=phone)
    message.set_subject("Email from portfolio")
    message.set_html(body)
    message.set_text(body)
    message.set_from("{}".format(email))
    status, msg = sg.send(message)
    logging.info(status)
    return True


class MyBlog(webapp2.RequestHandler):
    def get(self):
        logging.info("##get call")
        template = env.get_template('index.html')
        self.response.write(template.render())

    def post(self):
        name = self.request.get('name')
        email = self.request.get('email')
        # logging.info("Email: %s" % email)
        phone = self.request.get('phone')
        message = self.request.get('message')

        sendgrid_mail(name, email, phone, message)


application = webapp2.WSGIApplication(
    routes=[
        ('/', MyBlog),
    ],
    debug=True
)
