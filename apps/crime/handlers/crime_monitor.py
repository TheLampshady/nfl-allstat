from base_handler import BaseHandler
from apps.data_hunter.hunters import CrimeHunterUSA


class StartMonitorHandler(BaseHandler):

    def get(self, source='usatoday'):

        if source == 'usatoday':
            crime_source = CrimeHunterUSA()

        results = crime_source.get_content()

        types = set()
        for result in results:
            types = set(types).union(set(result['category']))

        self.render_json(list(types))

