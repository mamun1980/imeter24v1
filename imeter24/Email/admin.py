# Admin module
from imeter24.site import site

from imeter24.Email.models import *
from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    '''We want to customize our admin display'''
    fieldsets = [
        ('User Information',    {'fields': ['username', 'password',]}),
        ('Accounting',    {'fields': [('status', 'accountid'),]}),
        ('info',    {'fields': ['domain', 'source', 'destination',]}),
		('Additional Info', {'fields': ['currentcount','maxcount','daystoholdemails']}),
		('Status',    {'fields': ['accountsize','messagecount', 'last_updated','last_updated_time', 'last_accessed','last_accessed_time',]}),
        ('options', {'fields': [('mailscanner', 'virusscanner', 'poweruser', 'action'),]}),
    ]
    list_display = ('username', 'alias', 'ok', 'accountid', 'domain', 'source', 'destination','currentcount','messagecount', 'accountsize','last_accessed' )
    search_fields = ['username', '=password','domain', 'source', 'destination', '=accountid',]
    ordering = ('-currentcount','username',)
#    radio_fields = {'action': admin.VERTICAL}

    def alias(self, obj):
        return obj.password == 'alias'
    alias.short_description = 'alias?'
    alias.boolean = True

    def ok(self, obj):
        return obj.status == True
    ok.short_description = 'ok?'
    ok.boolean = True


site.register(Users, UserAdmin)


class IpBlockAdmin(admin.ModelAdmin):
    '''We want to customize our admin display'''
    fieldsets = [
        ('Program Information',    {'fields': ['program', 'ipaddress','action']}),
		('Comments',    {'fields': ['comments']}),

    ]
    list_display = ('ipaddress','action','program','comments' )
    search_fields = ['program','ipaddress','action','comments']
    ordering = ('action','ipaddress',)

site.register(IpBlock, IpBlockAdmin)

class BlackListServersAdmin(admin.ModelAdmin):
    '''We want to customize our admin display'''
    fieldsets = [
        ('Server Information',    {'fields': [('server','active'),'servername','serverlink']}),
		('Comments',    {'fields': ['comments']}),

    ]
    list_display = ('server','active','servername','serverlink','comments' )
    search_fields = ['server','servername','serverlink','comments']



site.register(BlackListServers, BlackListServersAdmin)


class IpCountAdmin(admin.ModelAdmin):
    '''We want to customize our admin display'''
    fieldsets = [
        ('Program Information',    {'fields': ['ipaddress','counthour', 'counttotal',]}),
		('Comments',    {'fields': ['comments']}),

    ]
    list_display = ('ipaddress','counttotal','counthour','comments' )
    search_fields = ['ipaddress','counthour','counttotal','comments' ]
    ordering = ('-counttotal','-counthour','ipaddress',)

site.register(IpCount, IpCountAdmin)


class TMDA_Whitelist_Admin(admin.ModelAdmin):
    '''We want to customize our admin display'''
    fieldsets = [
        ('TMDA Whitelist Information',    {'fields': ['username', 'address',]}),


    ]
    list_display = ('id', 'username','address', )
    search_fields = ['username','address',]
    ordering = ('username','address',)

site.register(TMDA_Whitelist, TMDA_Whitelist_Admin)

class TMDA_Blacklist_Admin(admin.ModelAdmin):
    '''We want to customize our admin display'''
    fieldsets = [
        ('TMDA Blacklist Information',    {'fields': ['username', 'address',]}),


    ]
    list_display = ('id', 'username','address', )
    search_fields = ['username','address',]
    ordering = ('username','address',)

site.register(TMDA_Blacklist, TMDA_Blacklist_Admin)
