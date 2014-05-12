from __future__ import absolute_import

import os

from .local import *

INSTALLED_APPS += ('storages',)

# ------------------------------------
#    AWS credentials (for both static and media)
# ------------------------------------

AWS_ACCESS_KEY_ID       = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY   = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_STORAGE_DOMAIN      = os.environ.get('AWS_STORAGE_DOMAIN')

# allows conditional upload (needs dateutil)
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False

# ------------------------------------
#    Static files
# ------------------------------------

DEFAULT_FILE_STORAGE = 'nextmng.common.s3utils.MediaStorage'
STATICFILES_STORAGE  = 'nextmng.common.s3utils.StaticStorage'

# media files (images uploaded by users)
BOTO_MEDIA_LOCATION   = 'media' # this only impacts unversioned storage
MEDIA_URL = 'https://%s.s3.amazonaws.com/%s/' % (AWS_STORAGE_BUCKET_NAME,BOTO_MEDIA_LOCATION)

# static assets
BOTO_STATIC_LOCATION   = 'static' # this only impacts unversioned storagee
STATIC_URL = 'https://%s.s3.amazonaws.com/%s/' % (AWS_STORAGE_BUCKET_NAME,BOTO_MEDIA_LOCATION)
