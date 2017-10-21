#Imeter Contacts Admin module
from __future__ import absolute_import

from imeter24.site import site

from django.db import models
from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.forms import TextInput, Textarea
from django.forms.models import BaseInlineFormSet


from imeter24.Contacts.models import Contacts,Contacts_Phone,Contacts_Email,Contacts_Distribution
from imeter24.Common.models import *
from django.contrib import admin

from django.forms import TextInput, Textarea

from imeter24.Config.models import Config_Data,Config_Contact_Type,Config_Payment_Terms,Config_Email_Type,Config_Delivery_Type,Distribution_Type
from imeter24.Config.models import Currency_Type,Phone_Type

class Contacts_Phone_Inline(admin.TabularInline):
	model = Contacts_Phone
	extra = 1

class Contacts_Email_Inline(admin.TabularInline):
	model = Contacts_Email
	extra = 1

class Contacts_Distribution_Inline(admin.TabularInline):
	model = Contacts_Distribution
	extra = 1


class Contacts_Admin(admin.ModelAdmin):
	'''We want to customize our admin display'''

	#readonly_fields = ('terms',)
	readonly_fields = ('record_created',)

	formfield_overrides = {
		models.CharField: {'widget': TextInput(attrs={'size':'40','style': 'height: 1em;'})},
		models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':40,'style': 'height: 1em;'})},
		}

	inlines = [Contacts_Phone_Inline, Contacts_Email_Inline, Contacts_Distribution_Inline, ]

	fieldsets = (
		('Info', {
			'fields': ( ('customer_name', ),
				('attention_to'),
				('address_1'),
				('address_2'),
				('city', 'province', 'postal_code', 'country'),
				('terms', 'contact_type'),
				('currency_type',  'foreign_account'),
				('record_created', 'last_activity',)
			),
		}),
#Phone info goes here?
		('Tax Info', {
#            'classes': ('collapse',),
			'fields': (('gst_tax_exempt', 'pst_tax_exempt', 'hst_tax_exempt'),
				('gst_number', 'pst_number', 'hst_number'),
			),
		}),
		('Shipping Info', {
#            'classes': ('collapse',),
			'fields': (('delivery_type','ship_collect', 'fob'),),
		}),
		('Account Payable Info', {
#            'classes': ('collapse',),
			'fields': ('ap_contact',),
		}),
		('Comments', {
#            'classes': ('collapse',),
			'fields': ('webpage','comments',),
		}),
	)

	list_display = ( 'accountid', 'customer_name','attention_to','address_1', 'address_2', 'city', 'province', 'postal_code', 'country','record_created', 'last_activity',)
	#search_fields = ['customer_name', 'accountid', 'attention_to']
	search_fields = ['customer_name', 'attention_to','address_1', 'address_2', 'city', 'province', 'postal_code']
	list_per_page = 100
	index = True

	#contact_type_comments = contact_type.objects.values('comments')


site.register(Contacts, Contacts_Admin)


class Login_Admin(admin.ModelAdmin):
	'''We want to customize our admin display'''
	readonly_fields = ('record_created',)

	formfield_overrides = {
		models.CharField: {'widget': TextInput(attrs={'size':'40','style': 'height: 1em;'})},
		models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':40,'style': 'height: 1em;'})},
		}

	fieldsets = (
		('Info', {
			'fields': ( ('login_password', 'login_status' ),
				('vpn_ip'),
				('remote_ip'),
				('inside_ip'),
				('soldto'),
				('siteid'),
				('locationid'),
				('record_created','last_login','last_logout'),

			),
		}),
		('Comments', {
			'fields': ( 'comments',),
			}),
	)

	def customer_name_sold_to(self, obj):
		if (obj.soldto):
			return obj.soldto.customer_name
		return None
	customer_name_sold_to.short_description = "Sold To"


	list_display = ('customer_name_sold_to','locationid', 'login_status', 'vpn_ip', 'last_login', 'last_logout')
	search_fields = ['customer_name_sold_to','locationid']
	ordering = ('-login','login_status','last_login')
	index = False
	list_per_page = 100

	#contact_type_comments = contact_type.objects.values('comments')
