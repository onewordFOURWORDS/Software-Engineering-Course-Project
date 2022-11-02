from cgitb import html
from flask_mail import Message
from app import mail
from flask import render_template
from app import app
from threading import Thread


def send_email(subject, sender, recipients, text_body, html_body):
    """
    Provides the function to send emails to a recipient.

    :param subject: email subject line
    :type subject: string
    :param sender: address the email is sent from
    :type sender: string
    :param recipients: the email address(es) the email is sent from
    :type recipients: list of string(s)
    :param text_body: plaintext email body
    :type text_body: string
    :param html_body: HTML formatted email body
    :type html_body: string
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        "[SSBM] Reset Your Password",
        sender=app.config["ADMINS"][0],
        recipients=[user.email],
        text_body=render_template("email/reset_password.txt", user=user, token=token),
        html_body=render_template("email/reset_password.html", user=user, token=token),
    )
