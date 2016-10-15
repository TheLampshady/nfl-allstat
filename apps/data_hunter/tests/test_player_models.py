from apps.data_hunter.common.utils import best_match_test
from apps.data_hunter.models.player_records import ArrestRecord
from apps.data_hunter.models.player_records import Player
from apps.data_hunter.tests.base import BaseTestCase
from apps.data_hunter.tests.mocks.mock_crimes import one_crime_mock
from apps.data_hunter.tests.mocks.mock_players import *


class TestPlayerModel(BaseTestCase):
    def setUp(self):
        super(TestPlayerModel, self).setUp()

        Player(**player_one).put()
        for player in sport_roster:
            Player(**player).put()

    def test_player_model_lookup(self):
        key_value = list()
        players = Player.query().fetch()

        for player in players:
            key_value.append((player.key.id(), player.name))

        self.assertEqual(len(key_value), 101, "Expect %s players. Got %s." % (1, len(players)))

    def test_overwrite_players(self):
        Player.overwrite_all([player_two])
        players = Player.query().fetch()
        self.assertEqual(len(players), 1, "Expect %s players. Got %s." % (1, len(players)))
        self.assertEqual(players[0].name, player_two['name'])

    def test_add_new_player(self):
        Player.update_insert_record(player_two).get_result()
        players = Player.query().fetch()
        new_player = Player.get_fuzzy_record(player_two['name'])

        self.assertEqual(len(players), 102, "Expect %s players. Got %s." % (1, len(players)))
        self.assertEqual(new_player.name, player_two['name'])

    def test_add_existing_player(self):
        Player.update_insert_record(player_one_double).get_result()
        players = Player.query().fetch()
        new_player = Player.get_fuzzy_record(player_one_double['name'])

        self.assertEqual(len(players), 101, "Expect %s players. Got %s." % (1, len(players)))
        self.assertEqual(new_player.team, player_one_double['team'])

    def test_fuzzy_lookup(self):
        key_value = list()
        players = Player.query().fetch()

        for player in players:
            key_value.append((player.key.id(), player.name))

        ratio, value = best_match_test("agiantname tosearch", key_value)
        print ratio

        self.assertTrue(ratio < 80, "Ration Algorithm is it too weak. Found %s" % value[1])

    def test_get_full_player_record_close_spelling(self):
        ArrestRecord(**one_crime_mock).put()
        player = Player.get_full_record("first las")

        self.assertTrue(player)
        self.assertEqual(len(player.arrest_record), 1)

