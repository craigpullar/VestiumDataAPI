from django.conf.urls import patterns, include, url
from api.api import *
from api.api_registration import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'api/', include(v1_api.urls)),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)