import webapp2

from apps.routes import handle_response_error
from handlers.data_monitor import DataMonitorHandler

data_source = [
    'usatoday',
    'sandiego',
    'pro',
    'fantasydata',
    'cbs',
]

app = webapp2.WSGIApplication([
    webapp2.Route('/hunter/start/<source:(%s)>' % '|'.join(data_source),
                  handler=DataMonitorHandler, name='start_player_scan'),
], debug=True)

app.error_handlers[403] = handle_response_error
app.error_handlers[404] = handle_response_error
app.error_handlers[500] = handle_response_error