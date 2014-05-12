from __future__ import absolute_import

import dj_database_url
import os

from .common import *

DEBUG = False
TEMPLATE_DEBUG = False
DEPLOY_MODE = 'production'

DATABASES = {
    'default': dj_database_url.config()
    }

# Django cache
CACHES = {
    'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': os.environ.get('MEMCACHIER_SERVERS').replace(',', ';'),
        'TIMEOUT': 500,
        'BINARY': True,
        'VERSION': 1,
        }
    }

# Bypass django cache configuration to contact pylibmc directly
os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';')
os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')


ADMINS = (
    ('riccardo', 'riccardo.sab@gmail.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/


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


# SENDGRID = {
#             'user': os.environ.get('SENDGRID_USER'),
#             'pass': os.environ.get('SENDGRID_PASS'),
#             }

POSTMASTER = {
            'key': os.environ.get('POSTMARK_API_KEY'),
            'sender': os.environ.get('POSTMARK_SENDER'),
            }

