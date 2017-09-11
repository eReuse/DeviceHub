from ereuse_devicehub.tests import TestStandard


class TestSchema(TestStandard):
    def test_schema(self):
        """Tests that the user can retrieve the schema."""
        result, status = self._get('schema', self.token)
        self.assert200(status)
