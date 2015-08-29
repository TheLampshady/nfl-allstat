from google.appengine.ext import ndb
from google.appengine.api import taskqueue


class Player(ndb.Model):
    """
    The big 3 ids for lead uniqueness.
    """
    TEAM_CHOICES = []

    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    position = ndb.StringProperty(required=True)
    team = ndb.StringProperty(required=True)
    points = ndb.IntegerProperty(required=True)

