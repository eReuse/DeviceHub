
from flask import Request, g
from flask import json, current_app
from flask.wrappers import _missing, _get_data

from app.exceptions import StandardError

PGP_MESSAGE = '-----BEGIN PGP SIGNED MESSAGE-----'


class RequestSignedJson(Request):
    """
        Adds the ability to parse signed JSON.

        It sets g.trusted_json to true if the json was correctly signed (verified), false otherwise.
    """

    def get_json(self, force=False, silent=False, cache=True):
        rv = getattr(self, '_cached_json', _missing)
        if rv is not _missing:
            return rv
        json_data = self.get_signed_json(cache)
        if json_data is None:
            json_data = super().get_json(force, silent, cache)
            g.trusted_json = False
        return json_data

    def get_signed_json(self, cache=True):
        """
        Verifies and returns a signed JSON. This code is strongly inspired by `flask.Request.get_json`

        :param cache:
        :return:
        """
        request_charset = self.mimetype_params.get('charset')
        encrypted_data = _get_data(self, cache)
        if not encrypted_data.startswith(PGP_MESSAGE.encode()):
            return None

        current_app.gpg.encoding = request_charset if request_charset is not None else 'utf-8'
        if not current_app.gpg.verify(encrypted_data):
            raise SignatureCannotBeVerified()
        decrypted_data = str(current_app.gpg.decrypt(encrypted_data))

        try:
            if request_charset is not None:
                rv = json.loads(decrypted_data, encoding=request_charset)
            else:
                rv = json.loads(decrypted_data)
        except ValueError as e:
                rv = self.on_json_loading_failed(e)
        if cache:
            self._cached_json = rv
        g.trusted_json = True
        return rv


class SignatureCannotBeVerified(StandardError):
    status_code = 400
    message = "The signature of the file cannot be verified. Have you uploaded the Public key?"
