from django.conf.urls import patterns, url, include
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns
from nextmng.main.views import S3Uploader

# Uploader API
urlpatterns = patterns(
    'nextmng.main.views',
    url(r'^prepare-s3upload$', S3Uploader.as_view(), name='s3upload'),
)