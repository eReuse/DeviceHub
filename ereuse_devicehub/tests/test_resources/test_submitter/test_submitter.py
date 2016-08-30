from unittest.mock import MagicMock

from assertpy import assert_that

from ereuse_devicehub.tests import TestStandard


class TestSubmitter(TestStandard):
    """
        Tests submitter through the GRD implementation.
    """

    def test_creation(self):
        assert_that(hasattr(self.app, 'grd_submitter_caller')).is_true()
        assert_that(hasattr(self.app, 'submit_events_to_grd')).is_true()
        assert_that(self.app.grd_submitter_caller.token).is_not_none()

    @staticmethod
    def mock_submit(submitter_class, token, app, mock_post):
        """
            Mocks Submitter._post and SubmitterCaller.submit, asserting the values that would have been sent to GRD.
        :return:
        """

        submitter = submitter_class(token, app)
        submitter._post = MagicMock()
        submitter._post.side_effect = mock_post

        def _mock_submit(event_id: str, database: str, resource_name: str):
            """Mocks SubmitterCaller.submit, directly calling Submitter."""
            submitter.submit(event_id, database, resource_name)
            assert_that(submitter._post.call_count).is_equal_to(1)

        return _mock_submit

    @staticmethod
    def mock_post(test, grd_resource, grd_url):
        def _mock_post(resource: dict, url: str):
            """Mocks Submitter._post, asserting entering values"""
            assert_that(resource['url']).contains('https://www.example.com/dht1/events/')
            assert_that(resource['byUser']).contains('https://www.example.com/accounts/')
            del resource['url']
            del resource['byUser']
            del resource['dhDate']
            assert_that(grd_resource).is_subset_of(resource)
            assert_that(url).is_equal_to(grd_url)
        return _mock_post

    def test_snapshot(self):
        # We load the expected result that is sent to GRD
        grd_resource = self.get_fixture(self.SNAPSHOT, 'vaio_grd')
        grd_url = 'https://sandbox.ereuse.org/api/devices/register'  # todo ensure requeriment
        # We prepare the call by mocking through mock_submit
        submitter_caller = self.app.grd_submitter_caller
        submitter_caller.submit = MagicMock()
        submitter_caller.submit.side_effect = self.mock_submit(submitter_caller.submitter, submitter_caller.token,
                                                               submitter_caller.app,
                                                               self.mock_post(self, grd_resource, grd_url))
        # We create the device, generating the devices:Register submission
        self.post_fixture(self.SNAPSHOT, '{}/{}'.format(self.DEVICE_EVENT, self.SNAPSHOT), 'vaio')
        assert_that(submitter_caller.submit.call_count).is_equal_to(1)
