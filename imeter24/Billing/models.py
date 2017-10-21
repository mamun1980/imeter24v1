from django.db import models

# Create your models here.

from imeter.Common.models import *

from imeter.Config.models import Config_Data,Config_Contact_Type,Config_Payment_Terms,Config_Email_Type,Config_Delivery_Type,Distribution_Type
from imeter.Config.models import Currency_Type,Phone_Type

class Billing_Recurring(models.Model):
	id					= models.AutoField(verbose_name='Account Number', null=False, blank=False, editable=False, primary_key=True)
	soldto 				= models.ForeignKey(Contacts,default = None,null=True, blank=True,related_name = 'billing_recurring_soldto')												#Sold to (Bill to) Info
	siteid 				= models.ForeignKey(Contacts,default = None,null=True, blank=True,related_name = 'billing_recurring_siteid')					#Physical Address that device is located
	locationid 			= models.ForeignKey(Contacts,default = None,null=True, blank=True,related_name = 'billing_recurring_locationid')	
	status 				= models.CharField(max_length=10, verbose_name='Billing Status', null=False, blank=False)
	last_invoiced 		= models.CharField(verbose_name='Last Invoiced', max_length=10, null=True, blank=True)
	last_invoiced_date 	= models.DateField(verbose_name='Last Invoiced On', null=True, blank=True)
	billing_cycle 		= models.IntegerField(verbose_name = 'Billing Cycle (Months)',null=True, blank=True)
	waive_setup_charges = models.BooleanField(verbose_name='Waive Setup Fee', blank=True, default=False)
	#accounting_sub_billing = 
	comments 			= models.CharField(verbose_name='Comments', max_length=64, null=True, blank=True)
	billing_email 		= models.EmailField(verbose_name='Billing Email', max_length=64, null=True, blank=True)
	
	
	class Meta:
		ordering = ['customer_name']
		db_table = u'billing_recurring'
		verbose_name = u"Recurring Billing"
		verbose_name_plural = u"Recurring Billing"

	def __unicode__(self):
		return self.soldto



class Billing_Recurring_Body(models.Model):
	billing_recurring	= models.ForeignKey(Contacts,related_name='billing_recurring_body', unique=False)
	qty					= models.ForeignKey(Phone_Type,default = 1,verbose_name='Type')
	billing_type		= models.CharField(verbose_name='Billing Type', max_length=20, null=True, blank=True)
	billing_description	= models.CharField(verbose_name='Description', max_length=10, null=True, blank=True)
	billing_amount 		= models.DecimalField(verbose_name='Base Billing Amount per Term', max_digits=10, decimal_places=2, null=True, blank=True)
	billing_total 		= models.DecimalField(verbose_name='Billing Total', max_digits=12, decimal_places=2, null=True, blank=True)
	
