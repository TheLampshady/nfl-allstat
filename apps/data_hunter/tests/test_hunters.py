import os
from mock import patch

from apps.data_hunter.tests.base import BaseTestCase
from apps.data_hunter.hunters import CrimeHunterUSA

file_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'mocks/mock_site.html')

mock_site = open(file_path, 'r').read()


class TestMonitorModel(BaseTestCase):

    patch_request = patch.object(CrimeHunterUSA, 'request_content')

    def setUp(self):

        self.mock_request = self.patch_request.start()
        self.mock_request.return_value = mock_site

        super(TestMonitorModel, self).setUp()

    def tearDown(self):
        self.patch_request.stop()

    def test_hunter_parses_site(self):
        test_hunter = CrimeHunterUSA()
        result = test_hunter.get_content()
        print len(result)