from google.appengine.ext import ndb


class InjuryRecord(ndb.Model):
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
    modifier = ndb.IntegerProperty(default=1)


    def get_modifier(self):
        #TODO refine catagories
        #TODO add modifiers Ex: 1.05
        #TODO 7 year Itch min modifier 1.01
        return 1

