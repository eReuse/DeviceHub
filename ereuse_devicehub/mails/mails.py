from flask import Blueprint, render_template
from pydash import defaults

"""
Templates for mails.
"""
mails = Blueprint('Mails', __name__, template_folder='templates', static_folder='static',
                  static_url_path='/mails/static')


def render_mail_template(title: str, template_name: str, recipient: dict, **context):
    """Adds default template variables and renders the template."""
    context = defaults(context, {
        'recipient': recipient,
        'title': title

    })
    return render_template(template_name, **context)
