from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nextmng.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    # REST API
    url(r'^api/', include('nextmng.urls_api', namespace='next_api')),

    # All
    url('', include('nextmng.main.urls', namespace="nextmng.main", app_name="nextmng.main")),
    
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()