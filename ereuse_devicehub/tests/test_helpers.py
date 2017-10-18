from assertpy import assert_that

from ereuse_devicehub.mails.mails import mails
from ereuse_devicehub.tests import TestStandard


class TestHelpers(TestStandard):
    def test_get_static_as_string(self):
        """
        Tests that get_static_as_string gets a file from the static
        folder from the current app and then from the blueprint, if the first does not have the file.
        """
        with self.app.app_context():
            # SetUp() already set the self.app.static_folder to a sub folder in the tests folder
            # In that folder there is a 'mail-style.css' file so we should be able to get it
            css = mails.get_static_as_string('mail-style.css')
            assert_that(css).contains('Overridden file!')
            # Now, if we don't set the static_folder within the app (for example when running DeviceHub
            # without configuring it), it should load the blueprint's default 'mail-style.css'
            self.app.static_folder = None
            css = mails.get_static_as_string('mail-style.css')
            assert_that(css).contains('Just an empty file')
            # If none of them have set a static_folder, just throw an error
            # In this case the error will be provoked by inner os.path.join(None,None)
            # Note that if they have the folder set *but* not the file this process is the same
            # however the following error changes from TypeError to FileNotFoundError
            mails.static_folder = None
            self.assertRaises(TypeError, mails.get_static_as_string, 'mail-style.css')
