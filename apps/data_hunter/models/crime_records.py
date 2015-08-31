from google.appengine.ext import ndb
from datetime import datetime

class ArrestRecord(ndb.Model):
    """
    The big 3 ids for lead uniqueness.
    """
    CASE_TYPE_CHOICES = []

    player_id = ndb.IntegerProperty(required=True)
    date_recorded = ndb.DateProperty(required=True)
    case_type = ndb.StringProperty(required=True)
    #case_type = ndb.StringProperty(required=True, choices=CASE_TYPE_CHOICES)
    outcome = ndb.StringProperty(required=True)
    category = ndb.StringProperty(repeated=True)
    description = ndb.StringProperty(required=True)
    modifier = ndb.IntegerProperty(default=1)

    @classmethod
    def update_insert_record(cls, key, attribute):
        date_recorded = datetime.strptime(attribute['date_recorded'], "%Y-%m-%d").date()
        crime_record = cls(
            player_id=key,
            date_recorded=date_recorded,
            case_type=attribute['case_type'],
            category=attribute['category'],
            description=attribute['description'],
            outcome=attribute['outcome'],
        )
        crime_record.put()

    @classmethod
    def get_by_player_id(cls, key):
        return cls.query(cls.player_id == key).fetch()

    def get_modifier(self):
        #TODO refine catagories
        #TODO add modifiers Ex: 1.05
        #TODO 7 year Itch min modifier 1.01
        return 1

