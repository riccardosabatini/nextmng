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
            'key': os.environ.get('POSTMARK_API_KEY'),
            'sender': os.environ.get('POSTMARK_SENDER'),
            }

DEPOT_DIR  = os.environ.get("DEPOT_DIR", None)


# ------------------------------------
#    Celery
# ------------------------------------
from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'check-deposit-task': {
        'task': 'nextmng.main.tasks.check_deposit_task',
        'schedule': timedelta(seconds=10),
    },
}

CELERY_TIMEZONE = 'UTC'
