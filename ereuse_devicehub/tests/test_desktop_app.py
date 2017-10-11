from assertpy import assert_that
from ereuse_devicehub.tests import TestStandard


class TestDesktopApp(TestStandard):
    def test_desktop_app(self):
        """
        Tests getting the information for the desktop-app and an attached file.

        Desktop app generates the information by the installers name in <static_folder>/desktop-app.
        """
        # Note that we don't need to perform log in
        config, status = self._get('desktop-app')
        self.assert200(status)
        assert_that(config).has_version('0.1.0')
        assert_that(config).has_files([
            {'url': '/static/desktop_app/eReuse.org-DesktopApp_0.1.0_ia32.deb', 'architecture': 'ia32', 'type': 'deb'}])
        response = self.test_client.get(config['files'][0]['url'])
        self.assert200(response.status_code)
        assert_that(response).has_content_type('application/x-debian-package')
        assert_that(response).has_data(b'1')
