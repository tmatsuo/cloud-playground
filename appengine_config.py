"""App Engine configuration file."""

import json
import re


from mimic.__mimic import common
from mimic.__mimic import datastore_tree
from mimic.__mimic import mimic

import caching_urlfetch_tree
import settings

from google.appengine.api import app_identity


# our current app id
app_id = app_identity.get_application_id()

if common.IsDevMode() or app_id == settings.PLAYGROUND_APP_ID:
  mimic_CREATE_TREE_FUNC = datastore_tree.DatastoreTree
else:
  mimic_CREATE_TREE_FUNC = caching_urlfetch_tree.CachingUrlFetchTree

# pylint: disable-msg=g-bad-name
mimic_JSON_ENCODER = json.JSONEncoder()
mimic_JSON_ENCODER.indent = 4
mimic_JSON_ENCODER.sort_keys = True

mimic_NAMESPACE = '_playground'

# keep in sync with app/js/controllers.js
mimic_PROJECT_ID_QUERY_PARAM = '_mimic_project'

mimic_PROJECT_ID_FROM_PATH_INFO_RE = re.compile('/playground/p/(.+?)/')

if common.IsDevMode():
  scheme = 'http'
else:
  scheme = 'https'

if settings.PLAYGROUND_USER_CONTENT_HOST:
  mimic_ALLOWED_USER_CONTENT_HOSTS = [settings.PLAYGROUND_USER_CONTENT_HOST]
else:
  mimic_ALLOWED_USER_CONTENT_HOSTS = None

mimic_CORS_ALLOWED_ORIGINS = ['{0}://{1}'.format(scheme, h)
                              for h in settings.PLAYGROUND_HOSTS]

mimic_CORS_ALLOWED_HEADERS = 'Origin, X-XSRF-Token, X-Requested-With, Accept, Content-Type'

# pylint: disable-msg=C6409
def namespace_manager_default_namespace_for_request():
  return mimic.GetNamespace()
