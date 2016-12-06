from ereuse_devicehub.resources.submitter.submitter import Submitter
from ereuse_devicehub.resources.submitter.translator import Translator


class DeviceHubSubmitter(Submitter):
    def __init__(self, token: str, app: 'DeviceHub', domain: str, translator: Translator, debug=False):
        auth = Auth(domain, account['username'], account['password'], 'api-token-auth/', 'Token')
        super().__init__(token, app, domain, translator, auth, debug)


class MigrateTranslator():
    def translate(self, database: str, migrate: dict) -> list:
        del migrate['events']
        return migrate
