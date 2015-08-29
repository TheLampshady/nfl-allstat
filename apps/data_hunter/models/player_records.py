from google.appengine.ext import ndb
from crime_records import ArrestRecord
from injury_records import InjuryRecord
from fantasy_records import FantasyRecord


class Player(ndb.Model):
    """
    Player states nd modifiers
    """
    TEAM_CHOICES = []

    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    name = ndb.StringProperty(required=True)
    position = ndb.StringProperty(required=True)
    #position_rank = ndb.StringProperty(default=0)
    team = ndb.StringProperty(required=True)
    jersey = ndb.IntegerProperty(default=0)
    bye_week = ndb.IntegerProperty(default=0)
    image = ndb.StringProperty()

    #fantasy = ndb.StructuredProperty(FantasyRecord)
    #arrest_record = ndb.StructuredProperty(ArrestRecord, repeated=True)
    #injury_record = ndb.StructuredProperty(InjuryRecord, repeated=True)
    arrest_modifier = ndb.IntegerProperty(default=1)

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