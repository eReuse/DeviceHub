from os import path
from urllib.parse import urlparse


class UrlParse:
    @staticmethod
    def get_database(base_url: str) -> str:
        """
            Obtains the database from a DeviceHub URL
            @:param base_url: An URL without any resource path.
        """
        if base_url[-1] == '/':
            base_url = base_url[:-1]
        return path.split(urlparse(base_url).path)[1]
