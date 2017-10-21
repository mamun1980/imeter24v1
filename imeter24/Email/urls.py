from django.conf.urls import *


urlpatterns = patterns('scom.Email.views',
    (r'^index$', 'index'),
    (r'^add/$', 'add'),
    (r'^delete/$', 'delete'),
    (r'^$', 'index'),
)
