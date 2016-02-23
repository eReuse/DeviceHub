from tests import TestStandard


class TestPlaces(TestStandard):
    def setUp(self, settings_file=None, url_converters=None):
        super(TestPlaces, self).setUp(settings_file, url_converters)

    def test_create_place_with_coordinates(self):
        place = self.get_fixture(self.PLACES, 'place')
        self.post_and_check('places', place)

