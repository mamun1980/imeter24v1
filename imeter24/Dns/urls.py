from django.conf.urls import *


urlpatterns = patterns('scom.Dns.views',
    (r'^$', 'index'),
    (r'^index/$', 'index'),
    (r'^enter/$', 'enter'),
    url(r'^create/$', 'create', name='createview'),
    url(r'^info/$', 'info', name='infoview'), 
)
