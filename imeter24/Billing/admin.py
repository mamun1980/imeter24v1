# Admin module
from django.db import models
from imeter24.site import admin_site

from imeter24.Billing import Billing_Recurring
from imeter24.Contacts.models import Contacts,Contacts_Phone,Contacts_Email,Contacts_Distribution,Login
from imeter24.Common.models import *
from django.contrib import admin

from django.forms import TextInput, Textarea

from imeter.Config.models import Config_Data,Config_Contact_Type,Config_Payment_Terms,Config_Email_Type,Config_Delivery_Type,Distribution_Type
from imeter.Config.models import Currency_Type,Phone_Type

class Billing_Recurring_Inline(admin.TabularInline):
	model = Billing_Recurring_body
	extra = 1


class Billing_Recurring_Admin(admin.ModelAdmin):
	'''We want to customize our admin display'''

	#readonly_fields = ('terms',)
	readonly_fields = ('record_created',)

	formfield_overrides = {
		models.CharField: {'widget': TextInput(attrs={'size':'40','style': 'height: 1em;'})},
		models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':40,'style': 'height: 1em;'})},
		}

	inlines = [Billing_Recurring_Inline, ]

	fieldsets = (
		('Info', {
			'fields': ( ('soldto', ),
				('siteid'),
				('locationid'),
				('status'),
				('last_invoiced','last_invoiced_date'),
				('billing_cycle','waive_setup_charges'),
				('comments'),
				('billing_email',)
			),
		}),

	list_display = ( 'id', 'soldto','last_invoiced','last_invoiced_date','billing_cycle','comments')
	search_fields = ['soldto',]
	list_per_page = 100

	#contact_type_comments = contact_type.objects.values('comments')


admin_site.register(Billing_Recurring, Billing_Recurring_Admin)
