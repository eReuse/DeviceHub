from flask import Blueprint, render_template
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
        'title': TITLES[template_name]

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


email_dispatched.connect(log_message)
