import webapp2
from apps.routes import handle_response_error
from handlers.home import HomePage

route_config = {
    'template_path': "apps/showboat/templates",
    'environment_args': {
        'autoescape': True,
    },
}


_APP = webapp2.WSGIApplication(
    [
        webapp2.Route('/', handler=HomePage, name='home'),
    ], debug=True, config=route_config)



_APP.error_handlers[403] = handle_response_error
_APP.error_handlers[404] = handle_response_error
_APP.error_handlers[500] = handle_response_error
