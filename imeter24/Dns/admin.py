# Admin module
from imeter24.site import admin_site

from imeter24.Dns.models import DNS_Data, zonesorted
from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    '''We want to customize our admin display'''
    fieldsets = [
        ('Zone Data',    {'fields': ['zone', 'type', 'host', 'data',]}),
        ('Extended Options',    {'fields': [('ttl', 'mx_priority', 'primary_ns', 'resp_person'), ('serial', 'refresh','retry', 'expire', 'minimum'), ]}),
        ('Accounting Information',    {'fields': [('status', 'accountid'),]}),
    ]
    list_display = ('id', 'zone', 'ttl', 'type', 'host', 'data', 'mx_priority', 'primary_ns', 'resp_person', 'serial', 'refresh','retry', 'expire', 'minimum', 'status', 'accountid',)
    search_fields = ['zone','=type', 'host', 'data', 'accountid', ]



admin_site.register(DNS_Data, UserAdmin)
