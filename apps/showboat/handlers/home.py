from apps.handlers.base import BaseHandler


class HomePage(BaseHandler):
    def get(self):
        self.render("index.html")




