from apps.base_handler import BaseHandler


class HomePage(BaseHandler):
    def get(self):
        self.render("index.html")




