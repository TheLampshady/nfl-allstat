from google.appengine.ext import ndb
from google.appengine.api import taskqueue



class ArrestRecord(ndb.Model):
    """
    The big 3 ids for lead uniqueness.
    """
    CASE_TYPE_CHOICES = []

    date_filed = ndb.DateProperty(required=True)
    case_type = ndb.StringProperty(required=True)
    #case_type = ndb.StringProperty(required=True, choices=CASE_TYPE_CHOICES)
    outcome = ndb.StringProperty(required=True)
    category = ndb.StringProperty(repeated=True)
    description = ndb.StringProperty(required=True)

