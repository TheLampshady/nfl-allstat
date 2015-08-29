import logging
import os
import webapp2
import jinja2


TEMPLATE_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'templates')

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_PATH),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
)


class HomePage(webapp2.RequestHandler):
    def get(self):
        self.render("index.html")

    def render(self, template, **kwargs):
        template = JINJA_ENVIRONMENT.get_template(template)
        self.response.write(template.render(kwargs))


app = webapp2.WSGIApplication(
    [
        webapp2.Route('/', handler=HomePage, name='home'),
    ], debug=True)


# ## setting a global request so that uri_for can work
request = webapp2.Request({})
request.app = app
app.set_globals(app=app, request=request)


def handle_response_error(request, response, exception):
    from webapp2_extras import jinja2 as webapp_jinja2

    logging.exception(exception)
    # If the exception is a HTTPException, use its error code else a generic 500 error code
    status_code = exception.code if isinstance(exception, webapp2.HTTPException) else 500

    j = webapp_jinja2.Jinja2(app, config={'template_path': TEMPLATE_PATH})
    t = j.render_template(str(status_code) + '.html')

    response.write(t)
    response.set_status(status_code)


app.error_handlers[403] = handle_response_error
app.error_handlers[404] = handle_response_error
app.error_handlers[500] = handle_response_error
