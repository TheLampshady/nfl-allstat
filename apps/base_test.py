import unittest
import logging
import webapp2
import webtest
from google.appengine.ext import testbed, ndb
from apps.routes import _APP

logging.basicConfig()


class BaseTestCase(unittest.TestCase):
    """Base Test"""

    def setUp(self, app=None):

        self.init_testbed()
        self.app = app if app else _APP
        self.testapp = webtest.TestApp(self.app)

        ndb.get_context().clear_cache()
        self.maxDiff = None

    def tearDown(self):
        self.testbed.deactivate()

    def init_testbed(self):
        self.testbed = testbed.Testbed()
        self.testbed.setup_env(current_version_id='testbed.version')
        self.testbed.activate()

        # add in services we will be testing
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_logservice_stub()
        self.testbed.init_user_stub()
        self.testbed.init_search_stub()

        self.testbed.init_taskqueue_stub(root_path=".")
        self.taskqueue_stub = self.testbed.get_stub(testbed.TASKQUEUE_SERVICE_NAME)


