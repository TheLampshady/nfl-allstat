import os
import json
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        os.path.abspath(os.path.join(os.path.dirname(__file__), '../templates'))),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
)


class BaseHandler(webapp2.RequestHandler):

    def render(self, template, **kwargs):
        template = JINJA_ENVIRONMENT.get_template(template)
        self.response.write(template.render(kwargs))

    def render_json(self, content):
        self.response.headers.add('Content-Type', 'application/json')
        self.response.write(json.dumps(content))