from mock import patch

from apps.data_hunter.tests.base import *
from apps.data_hunter.models.player_records import Player
from apps.data_hunter.models.crime_records import ArrestRecord
from apps.data_hunter.tests.mocks.mock_players import *
from apps.data_hunter.tests.mocks.mock_crimes import *


mock_site = open_mock_file("crime_json.json")


class TestCrimeModel(BaseTestCase):
    def setUp(self):
        super(TestCrimeModel, self).setUp()

        Player(**player_one).put()

    def test_crime_model_insert_exist(self):
        key = Player.query().get().key.id()
        ArrestRecord.update_insert_record(key, one_category_crime)
        ArrestRecord.update_insert_record(key, two_category_crime)
        record_list = ArrestRecord.get_by_player_id(key)

        self.assertEqual(len(record_list), 2, "Expect %s players. Got %s." % (1, len(record_list)))
