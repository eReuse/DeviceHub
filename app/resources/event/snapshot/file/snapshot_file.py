from app.resources.event.snapshot.snapshot import Snapshot


class SnapshotFile(Snapshot):
    def __init__(self, encrypted_data):
        self.encrypted_data = encrypted_data
        self.string = None
        self.register = None

    def decrypt(self):
        import gnupg
        gpg = gnupg.GPG()
        gpg.encoding = 'utf-8'
        if not gpg.verify(self.encrypted_data):
            raise ValueError("Signature could not be verified!")
        self.string = str(gpg.decrypt(self.encrypted_data))

    def get_register_object(self):
        import json
        data = json.loads(self.string)
        if data['version'] == 1.0:
            from app.resources.event.register.translation1_0 import Translation1_0
            self.register = Translation1_0.translate(root)
        else:
            raise VersionNotSupportedError('Version ' + str(version) + ' is not supported')


class VersionNotSupportedError(object, Exception):
    pass
