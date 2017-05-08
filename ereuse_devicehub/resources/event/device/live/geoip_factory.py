from ereuse_devicehub.exceptions import StandardError
from geoip2 import webservice


class GeoIPFactory:
    MAXMIND_PREMIUM = 'maxmind premium'

    def __init__(self, app):
        """
        Initializes the service.

        :param app: Flask App
        """
        service = app.config.setdefault('GEO_IP', self.MAXMIND_PREMIUM)
        try:
            if service == self.MAXMIND_PREMIUM:
                ACCOUNT = app.config['MAXMIND_ACCOUNT']
            self.client = webservice.Client(ACCOUNT['user'], ACCOUNT['license key'])
        except KeyError as e:
            raise NotValidAccount() from e

    def __call__(self, data):
        """
        Translates the ip obtaining the data representing the location.
        :return:
        """
        return self.client.insights(data)


class NotValidAccount(StandardError):
    message = 'The account for the GEOIP service is invalid or it is not set in settings. For Maxmind set it as ' \
              '\'MAXMIND_ACCOUNT\' = {\'user\': int, \'license key\': string}'
