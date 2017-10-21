# Admin module
from imeter24.site import site

from imeter24.Config.models import Config_Data,Config_Contact_Type,Config_Payment_Terms,Config_Email_Type,Config_Delivery_Type,Distribution_Type
from imeter24.Config.models import Currency_Type,Phone_Type,Config_Hardware_Type
from django.contrib import admin


class ConfigAdmin(admin.ModelAdmin):
	'''We want to customize our admin display'''
	fieldsets = [
		('Config Data',    {'fields': ['variable', 'value', 'comments' ]}),
	]
	list_display = ('variable', 'value','comments')
	search_fields = ['variable', 'value','comments' ]



site.register(Config_Data, ConfigAdmin)


class Config_Contact_Type_Admin(admin.ModelAdmin):
	'''We want to customize our admin display'''
	fieldsets = [
		('Contact Type Data',    {'fields': ['type','comments']}),
	]
	list_display = ('id','type', 'comments',)
	search_fields = ['type', 'comments', ]



site.register(Config_Contact_Type, Config_Contact_Type_Admin)

# admin.site.register(Config_Contact_Type)

class Config_Payment_Terms_Admin(admin.ModelAdmin):
	'''We want to customize our admin display'''
	fieldsets = [
		('Type Data',    {'fields': ['type','comments']}),
	]
	list_display = ('id','type', 'comments',)
	search_fields = ['type', 'comments', ]



site.register(Config_Payment_Terms, Config_Payment_Terms_Admin)

class Config_Email_Type_Admin(admin.ModelAdmin):
	'''We want to customize our admin display'''
	fieldsets = [
		('Type Data',    {'fields': ['type','comments']}),
	]
	list_display = ('id','type', 'comments',)
	search_fields = ['type', 'comments', ]



site.register(Config_Email_Type, Config_Email_Type_Admin)

class Config_Delivery_Type_Admin(admin.ModelAdmin):
	'''We want to customize our admin display'''
	fieldsets = [
		('Type Data',    {'fields': ['type','comments']}),
	]
	list_display = ('id','type', 'comments',)
	search_fields = ['type', 'comments', ]



site.register(Config_Delivery_Type, Config_Delivery_Type_Admin)

class Distribution_Type_Admin(admin.ModelAdmin):
	'''We want to customize our admin display'''
	fieldsets = [
		('Type Data',    {'fields': ['type','comments']}),
	]
	list_display = ('id','type', 'comments',)
	search_fields = ['type', 'comments', ]



site.register(Distribution_Type, Distribution_Type_Admin)

class Currency_Type_Admin(admin.ModelAdmin):
	'''We want to customize our admin display'''
	fieldsets = [
		('Type Data',    {'fields': ['type','comments']}),
	]
	list_display = ('id','type', 'comments',)
	search_fields = ['type', 'comments', ]



site.register(Currency_Type, Currency_Type_Admin)


class Phone_Type_Admin(admin.ModelAdmin):
	'''We want to customize our admin display'''
	fieldsets = [
		('Type Data',    {'fields': ['type','comments']}),
	]
	list_display = ('id','type', 'comments',)
	search_fields = ['type', 'comments', ]



site.register(Phone_Type, Phone_Type_Admin)

class Config_Hardware_Type_Admin(admin.ModelAdmin):
	'''We want to customize our admin display'''
	fieldsets = [
		('Type Data',    {'fields': ['type','comments']}),
	]
	list_display = ('id','type', 'comments',)
	search_fields = ['type', 'comments', ]



site.register(Config_Hardware_Type, Config_Hardware_Type_Admin)
