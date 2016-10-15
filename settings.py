import os
from google.appengine.api import app_identity

SERVER_SOFTWARE = os.environ.get('SERVER_SOFTWARE', 'Unknown')
VERSION = os.environ.get('CURRENT_VERSION_ID', 'dev').split('.')[0]
MODULE = os.environ.get('CURRENT_MODULE_ID', 'default')

DEBUG = SERVER_SOFTWARE == 'Unknown' or SERVER_SOFTWARE.startswith('Dev')
