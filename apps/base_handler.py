import webapp2
import json
from webapp2_extras import jinja2


class BaseHandler(webapp2.RedirectHandler):

    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.context = {
            'url_for': self.uri_for,
        }

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.Jinja2(app=self.app, config=self.app.config)

    def render(self, template):
        self.response.write(self.jinja2.render_template(template, **self.context))

    def render_json(self, content):
        self.response.headers.add('Content-Type', 'application/json')
        self.response.write(json.dumps(content))