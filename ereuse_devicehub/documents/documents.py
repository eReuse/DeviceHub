from eve.auth import requires_auth
from flask import Blueprint, request, render_template, Response, make_response
from flask_weasyprint import HTML, render_pdf
from lazy_object_proxy import identity

from ereuse_devicehub.exceptions import WrongQueryParam
from ereuse_devicehub.header_cache import header_cache
from ereuse_devicehub.rest import execute_get

"""
The documents blueprint offers several documents (in PDF format for example)
related to the resources in DeviceHub.

This module uses Weasyprint to generate PDFs. See static/style.css for more info.
"""
documents = Blueprint('Documents', __name__, template_folder='templates',
                      static_folder='static', static_url_path='/documents/static')


def generate_document(template: str, filename: str) -> Response:
    """Generates the document in PDF (default) or HTML if argument debug is True."""
    if request.args.get('debug', False, bool):
        response = make_response(template)  # HTML
    else:
        response = render_pdf(HTML(string=template), download_filename=filename)  # PDF
    return response


@documents.route('/<db>/documents/delivery-note')
@header_cache(expires=None)
def delivery_note(db: str) -> Response:
    """
    Gets a PDF containing a delivery note for the passed-in devices.
    :param db:
    :arg ids: A list of device ids.
    """
    requires_auth('resource')(identity)('devices')
    ids = request.args.getlist('ids')
    if not ids:
        raise WrongQueryParam('ids', 'Send some device ids.')
    query_params = {
        'where': {'_id': {'$in': ids}},
        'embedded': {'tests': 1, 'erasures': 1}
    }
    template_params = {
        'title': 'Delivery note',
        'devices': execute_get(db + '/devices', params=query_params)['_items'],
        'fields': (
            {'path': '_id', 'name': 'System ID'},
            {'path': '@type', 'name': 'Type'},
            {'path': 'serialNumber', 'name': 'S/N'},
        )
    }
    template = render_template('documents/delivery_note.html', **template_params)
    return generate_document(template, filename='delivery note.pdf')
