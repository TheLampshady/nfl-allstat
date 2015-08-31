from datetime import datetime

from google.appengine.api import taskqueue

from base_handler import BaseHandler
from ..configs.queue_configs import MONITOR_QUEUE
from apps.data_hunter.models.hunters.crime_hunters import CrimeHunterUSA
from apps.data_hunter.models.hunters.player_hunters import PlayerHunterCBS

class DataMonitorHandler(BaseHandler):

    def get(self, source):

        if source == 'usatoday':
            hunter_source = CrimeHunterUSA()
        elif source == 'cbs':
            hunter_source = PlayerHunterCBS()
        else:
            self.abort(404)
        results = hunter_source.get_content()

        hunter_source.save_content(results)

        #self.queue_add(self.request.path, hunter_source.type)
        self.render_json(list(results))


    @classmethod
    def queue_add(cls, url, hunter_type):

        info = dict(
            queue_name=MONITOR_QUEUE['name'],
            url=url
        )

        info['eta'] = datetime.now() + MONITOR_QUEUE['time_delta'][hunter_type]

        return taskqueue.add(**info)

