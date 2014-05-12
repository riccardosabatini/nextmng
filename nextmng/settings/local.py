from __future__ import absolute_import
import os

from .common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEPLOY_MODE    = 'local'

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
            },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'nextmng.log',
            'formatter': 'simple'
            },
        },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
            },
        }
    }

if DEBUG:
    # make all loggers use the console.
    for logger in LOGGING['loggers']:
        LOGGING['loggers'][logger]['handlers'] = ['console']
        
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

ADMINS = (
    ('riccardo', 'riccardo.sab@gmail.com'),
)

MANAGERS = ADMINS



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/


MEDIA_URL   = '/media/'
MEDIA_ROOT  = os.path.join(os.path.dirname(BASE_DIR), '.media')

STATIC_URL  = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


REST_API_DOCS_ENABLE = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

# SENDGRID = {
#             'user': os.environ.get('SENDGRID_USER'),
#             'pass': os.environ.get('SENDGRID_PASS'),
#             }

POSTMASTER = {
            'key': os.environ.get('POSTMASTER_KEY'),
            'sender': os.environ.get('POSTMASTER_SENDER'),
            }