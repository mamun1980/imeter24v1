from django.conf.urls import url
from django.contrib import admin
from imeter24.site import site

from MeterRead.views import *

from imeter24.MeterRead.sites import MeterReadSite
meter_read_site = MeterReadSite(name='user')

urlpatterns = [
    url(r'^MeterRead/meterread/$', redirect_to_dashboard),
    url(r'^', site.urls),
    url(r'^user/', meter_read_site.urls),
]
