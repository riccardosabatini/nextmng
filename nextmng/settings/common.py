"""
Django settings for nextmng project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=g#tv+3@)t9z2h)zz-rfb001_g1x87yi+4bj!-wnd940#my3!8'

# Application definition

INSTALLED_APPS = (
    'djangocms_admin_style',
    #'admin_shortcuts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'nextmng.main'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'nextmng.urls'

WSGI_APPLICATION = 'nextmng.wsgi.application'


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Rome'
 
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
 
SITE_ID = 1
 
# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
 
# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True
 
# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True
 
# AngularJS will complains is we append slashes
APPEND_SLASH = False  

