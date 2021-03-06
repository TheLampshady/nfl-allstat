from mock import patch

from apps.data_hunter.tests.base import *
from apps.data_hunter.models.hunters.crime_hunters import CrimeHunterUSA
from apps.data_hunter.models.hunters.player_hunters import PlayerHunterCBS

mock_site = open_mock_file("mock_site.html")
mock_cbs_json = open_mock_file("mock_cbs_partial.json")


class TestHunter(BaseTestCase):

    patch_crime_request = patch.object(CrimeHunterUSA, 'request_content')
    patch_player_request = patch.object(PlayerHunterCBS, 'request_content')

    def setUp(self):

        self.mock_crime_request = self.patch_crime_request.start()
        self.mock_crime_request.return_value = mock_site

        self.mock_player_request = self.patch_player_request.start()
        self.mock_player_request.return_value = mock_cbs_json

        super(TestHunter, self).setUp()

    def tearDown(self):
        self.patch_crime_request.stop()
        #self.patch_player_request.stop()

    def test_hunter_parses_crime_site(self):
        test_hunter = CrimeHunterUSA()
        result = test_hunter.get_content()
        self.assertEqual(len(result), 36, "Expect %s Records. Got %s." % (36, len(result)))

    def test_hunter_parses_player_site(self):
        test_hunter = PlayerHunterCBS()
        result = test_hunter.get_content()
        self.assertEqual(len(result), 42, "Expect %s Records. Got %s." % (36, len(result)))

