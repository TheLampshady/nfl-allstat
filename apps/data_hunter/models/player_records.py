import logging

from google.appengine.ext import ndb
from apps.common.utils import best_match
from apps.data_hunter.models.crime_records import ArrestRecord


class Player(ndb.Model):
    """
    Player states nd modifiers
    """
    TEAM_CHOICES = []
    arrest_record = list()
    fantasy_record = list()
    injury_record = list()

    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    name = ndb.StringProperty(required=True)
    position = ndb.StringProperty(required=True)
    #position_rank = ndb.StringProperty(default=0)
    team = ndb.StringProperty(required=True)
    jersey = ndb.IntegerProperty(default=0)
    bye_week = ndb.IntegerProperty(default=0)
    image = ndb.StringProperty()
    arrest_modifier = ndb.IntegerProperty(default=1)

    @classmethod
    def get_full_record(cls, full_name):
        player_record = cls.get_fuzzy_record(full_name)
        if not player_record:
            return None

        player_key = Player.query().get().key.id()

        player_record.arrest_record = ArrestRecord.get_by_player_id(player_key)

        return player_record

    @classmethod
    def overwrite_all(cls, player_props_list):
        future_list = list()
        break_down = 10
        ndb.delete_multi(cls.query().fetch(keys_only=True))

        logging.info("Datastore Cleared")
        progress = 1
        progress_range = round(float(len(player_props_list)) / break_down)
        for player in player_props_list:
            progress += 1
            if progress_range and (float(progress) % progress_range == 0):
                logging.info("%s%% Complete" % (round(float(progress) / progress_range) * break_down))
            try:
                future_list.append(Player(**player).put_async())
            except:
                logging.warning("Player Error: %s" % player)

        ndb.Future.wait_all(future_list)
        logging.info("Save Completed")

    @classmethod
    def update_insert_record(cls, player):
        player_record = cls.get_fuzzy_record(player['name'])

        if player_record:
            for key, value in player.items():
                try:
                    setattr(player_record, key, value)
                except:
                    logging.warning("Cannot set: '%s'.%s to %s" %
                                    (player_record.name, key, value))
        else:
            player_record = cls(**player)

        return player_record.put_async()

    @classmethod
    def get_fuzzy_record(cls, search_name):
        key_value_list = list()
        players = cls.query().fetch()

        for player in players:
            key_value_list.append((player.key.id(), player.name))

        result = best_match(search_name, key_value_list, set_threshold=True)
        if not result:
            return None

        return cls.get_by_id(result[0])

    def get_player_relation_modifier(self):
        if self.position == 'QB':
            self.get_wr_average(team=self.team)
            self.get_wr_average_last_year(team=self.team)
            self.get_wr_modifier(team=self.team)
        if self.position == 'WR':
            self.get_qb_average(team=self.team)
            self.get_qb_average_last_year(team=self.team)
            self.get_qbs_modifier(team=self.team)
        return 1