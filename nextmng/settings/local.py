from __future__ import absolute_import
import os

from .common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEPLOY_MODE    = os.environ.get('DEPLOY_MODE', 'local'),

# ------------------------------------
#    Databases
# ------------------------------------

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DJANGO_DB_ENGINE'),
        'NAME': os.environ.get('DJANGO_DB_NAME'),
        'USER': os.environ.get('DJANGO_DB_USER'),
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD'),
        'HOST': os.environ.get('DJANGO_DB_HOST'),
        'PORT': os.environ.get('DJANGO_DB_PORT'),
    }
}

# ------------------------------------
#    Admins
# ------------------------------------

ADMINS = (
    ('riccardo', 'riccardo.sab@gmail.com'),
)

MANAGERS = ADMINS

# ------------------------------------
#    Static files
# ------------------------------------


MEDIA_ROOT = '.assets/media/'
MEDIA_URL = '/media/'

STATIC_ROOT = '.assets/static/'
STATIC_URL = '/static/'

REST_API_DOCS_ENABLE = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

# ------------------------------------
#    Services
# ------------------------------------

# SENDGRID = {
#             'user': os.environ.get('SENDGRID_USER'),
#             'pass': os.environ.get('SENDGRID_PASS'),
#             }

POSTMASTER = {
            'key': os.environ.get('POSTMASTER_KEY'),
            'sender': os.environ.get('POSTMASTER_SENDER'),
            }

