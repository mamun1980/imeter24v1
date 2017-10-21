#Imeter Contacts models.py

from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from imeter24.Common.models import *

from imeter24.Config.models import Config_Data,Config_Contact_Type,Config_Payment_Terms,Config_Email_Type,Config_Delivery_Type,Distribution_Type
from imeter24.Config.models import Currency_Type,Phone_Type

class Contacts(models.Model):
	accountid             = models.AutoField(verbose_name='Account Number', null=False, blank=False, editable=False, primary_key=True)
	customer_name         = models.CharField(max_length=64, verbose_name='Customer Name', null=False, blank=False)
	attention_to          = models.CharField(max_length=64, verbose_name='Attention To', null=True, blank=True)
	webpage               = models.URLField(max_length=200, null=True, blank=True)
	address_1             = models.CharField(max_length=64, verbose_name='Address Line 1', null=True, blank=True)
	address_2             = models.CharField(max_length=64, verbose_name='Address Line 2', null=True, blank=True)
	city                  = models.CharField(max_length=64, verbose_name='city', null=True, blank=True)
	province              = models.CharField(max_length=64, verbose_name='Province or State', null=True, blank=True,default='Ontario')
	country               = models.CharField(max_length=40, verbose_name='Country', null=True, blank=True,default='Canada')
	postal_code           = models.CharField(max_length=15, verbose_name='Postal Code or ZIP', null=True, blank=True)
	gst_tax_exempt        = models.BooleanField(verbose_name='GST Tax Exempt?', blank=False, default=False)
	hst_tax_exempt        = models.BooleanField(verbose_name='HST Tax Exempt?', blank=False, default=False)
	pst_tax_exempt        = models.BooleanField(verbose_name='PST Tax Exempt?', blank=False, default=False)
	terms                 = models.ForeignKey(Config_Payment_Terms, default = 1)
	gst_number            = models.CharField(max_length=17, verbose_name='GST number', null=True, blank=True)
	hst_number            = models.CharField(max_length=17, verbose_name='HST number', null=True, blank=True)
	contact_type          = models.ForeignKey(Config_Contact_Type,default = 1)
	pst_number            = models.CharField(max_length=11, verbose_name='PST number', null=True, blank=True)
	foreign_account       = models.CharField(max_length=30, verbose_name='Our Account # With Them', null=True, blank=True)
	delivery_type         = models.ForeignKey(Config_Delivery_Type,default = 1)
	ship_collect          = models.BooleanField(verbose_name="Ship Collect?", blank=False, default=False)
	currency_type         = models.ForeignKey(Currency_Type,default = 1)
	fob                   = models.CharField(max_length=50, verbose_name='FOB', null=True, blank=True,default = 'Oshawa, Ontario, Canada')
	ap_contact            = models.TextField(null=True, blank=True, verbose_name='AP contact info', help_text='Enter Accounts Payable contact name, number and e-mail.')
	comments              = models.TextField(null=True, blank=True, verbose_name='Comments')
	record_created        = models.DateField(null=True, blank=True,auto_now_add=True)
	last_activity         = models.DateField(null=True, blank=True)

	class Meta:
		ordering = ['customer_name']
		db_table = u'contacts'
		verbose_name = u"Contact"
		verbose_name_plural = u"Contacts"

	def __unicode__(self):
		return self.customer_name



class Contacts_Phone(models.Model):
	contact				= models.ForeignKey(Contacts, related_name='phone_number', unique=False)
	phone_type			= models.ForeignKey(Phone_Type, default = 1,verbose_name='Type')
	phone_number		= models.CharField(verbose_name='Phone Number', max_length=20, null=True, blank=True)
	phone_ext			= models.CharField(verbose_name='Extention', max_length=10, null=True, blank=True)

class Contacts_Email(models.Model):
	contact				= models.ForeignKey(Contacts, related_name='email_address', unique=False)
	email_type			= models.ForeignKey(Config_Email_Type, default = 1,verbose_name='Type')
	email_address		= models.CharField(verbose_name='Email Address', max_length=20, null=True, blank=True)

class Contacts_Distribution(models.Model):
	contact				= models.ForeignKey(Contacts, related_name='distribution', unique=False)
	distribution_type	= models.ForeignKey(Distribution_Type, default = 1, verbose_name='Distribution Type')
	distribution_data	= models.CharField(verbose_name='Distribution Data', max_length=64, null=True, blank=True)

status_choices = (
	('NEW', 'New Account (Guest Status)'),
	('UP', 'Account Logged In'),
	('DOWN', 'Account Logged Out'),
	('RAD', 'Radius Programming'),
)

alarm_choices_up = (
	('NONE', 'None'),
	('EMAIL','Email Notification'),
	('CALL', 'Call Notification'),
	('BOTH', 'Email & Call Notification'),
)

alarm_choices_down = (
	('NONE', 'None'),
	('EMAIL','Email Notification'),
	('CALL', 'Call Notification'),
	('BOTH', 'Email & Call Notification'),
)
