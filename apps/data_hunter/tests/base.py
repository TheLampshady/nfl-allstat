import os
import logging
from apps.base_test import BaseTestCase


logging.basicConfig()


class BaseHunterTestCase(BaseTestCase):
    """Base Test"""
    pass


def open_mock_file(file_name):
    file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'mocks/%s' % file_name)

    file_instance = open(file_path, 'r')
    content = file_instance.read()
    file_instance.close()
    return content