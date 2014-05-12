import storages.backends.s3boto

class MediaStorage(storages.backends.s3boto.S3BotoStorage):
  def __init__(self, *args, **kwargs):
    from django.conf import settings
    kwargs['location'] = settings.BOTO_MEDIA_LOCATION
    return super(MediaStorage, self).__init__(*args, **kwargs)

class StaticStorage(storages.backends.s3boto.S3BotoStorage):
  def __init__(self, *args, **kwargs):
    from django.conf import settings
    kwargs['location'] = settings.BOTO_STATIC_LOCATION
    return super(StaticStorage, self).__init__(*args, **kwargs)