import webapp2

from ..application import handle_response_error
from handlers.crime_monitor import StartMonitorHandler


app = webapp2.WSGIApplication([
    webapp2.Route('/crime/start', handler=StartMonitorHandler, name='start_scan'),
    webapp2.Route('/crime/start/<source:(usatoday|sandiego)>', handler=StartMonitorHandler, name='start_scan_source'),
], debug=True)

app.error_handlers[403] = handle_response_error
app.error_handlers[404] = handle_response_error
app.error_handlers[500] = handle_response_error