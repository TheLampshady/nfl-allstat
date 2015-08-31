import os
import json
import pickle
import unittest
import logging

import webapp2
import webtest


logging.basicConfig()


class BaseTestCase(unittest.TestCase):
    """Base Test"""

    def setUp(self):

        from apps.data_hunter.application import app
        from google.appengine.ext import testbed
        self.app = app

        ### setup request objects
        request = webapp2.Request({})
        request.app = self.app
        self.app.set_globals(app=self.app, request=request)

        self.testapp = webtest.TestApp(self.app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        ### declare services we will be testing
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_logservice_stub()
        self.testbed.init_user_stub()

        self.testbed.init_taskqueue_stub(root_path=".")
        self.taskqueue_stub = self.testbed.get_stub(testbed.TASKQUEUE_SERVICE_NAME)

    def tearDown(self):
        self.testbed.deactivate()

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