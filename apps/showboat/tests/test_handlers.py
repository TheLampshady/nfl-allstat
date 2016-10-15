from apps.showboat.tests.base import BaseShowboatTestCase
from apps.showboat.routes import _APP


class TestShowBoatHandlers(BaseShowboatTestCase):

    def setUp(self):
        super(TestShowBoatHandlers, self).setUp(app=_APP)

    def test_handler_renders(self):
        url = "/"

        response = self.testapp.get(url)
        self.assertEqual(response.status_code, 200)

