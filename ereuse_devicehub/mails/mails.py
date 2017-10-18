from contextlib import suppress
from smtplib import SMTPRecipientsRefused

from flask import Blueprint, current_app as app, render_template
from flask_mail import Message, email_dispatched
from pydash import defaults

"""
Templates for mails.
"""
mails = Blueprint('Mails', __name__, template_folder='templates', static_folder='static',
                  static_url_path='/mails/static')

TITLES = {
    'mails/reserve_for.html': 'New reservation of devices',
    'mails/reserve_notify.html': 'Your reservation',
    'mails/sell.html': 'New sold devices',
    'mails/cancel_reserve_for.html': 'Reservation canceled',
    'mails/cancel_reserve_notify.html': 'Reservation canceled'
}


def render_mail_template(template_name: str, recipient: dict, **context) -> (str, str):
    """Adds default template variables and renders the template."""
    context = defaults(context, {
        'recipient': recipient,
        'title': TITLES[template_name],
        'mail_style': mails.get_static_as_string('mail-style.css')
    })
    return render_template(template_name, **context), TITLES[template_name]


def create_email(template_name: str, recipient: dict, **context) -> Message:
    """Creates a mail with html."""
    html, title = render_mail_template(template_name, recipient, **context)
    return Message(html=html, recipients=[recipient['email']], subject=title)


# Log messages
# From http://pythonhosted.org/Flask-Mail/#signalling-support
def log_message(message: Message, app):
    app.logger.info('Sent message {} to {}.'.format(message.subject, message.recipients))


# noinspection PyPep8Naming
class suppressAndLogSendingException(suppress):
    """
    Catches and logs the exception when the mail server refuses to send the e-mail to all the recipients.
    """

    def __init__(self, message: Message):
        self.message = message
        super().__init__(SMTPRecipientsRefused)

    def __exit__(self, exctype, excinst, exctb):
        suppressed = super().__exit__(exctype, excinst, exctb)
        if suppressed:
            m = 'Couldn\'t send message {} because the server refused to send it to {}.'.format(self.message, excinst)
            app.logger.error(m)
        return suppressed


email_dispatched.connect(log_message)
