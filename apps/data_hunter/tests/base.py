import os
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

    def get_url(self, name, **kwargs):
        """
        use to resolve URL for any named path
        :param name: name of Route
        :param kwargs: fields required for Route
        :return: URL that matches
        """
        return webapp2.uri_for(name, **kwargs)


def open_mock_file(file_name):
    file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'mocks/%s' % file_name)

    file_instance = open(file_path, 'r')
    content = file_instance.read()
    file_instance.close()
    return content